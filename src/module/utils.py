import hashlib
import os
import platform
import random
import re
import socket
import string
from datetime import datetime
from io import BytesIO, StringIO
from pathlib import Path, PurePath
from re import Pattern
from threading import Thread
from typing import AnyStr, Type, TypeVar

import distro as distro
import psutil as psutil
import qrcode
import requests
from PIL import Image
from pyzbar.pyzbar import decode as pyzbar_decode
from rich.progress import track

from module.atomicwrites import atomic_write
from module.os_type import OSType


def is_port_in_use(_port: int, _host: str = '127.0.0.1') -> bool:
    """检查端口是否被占用

    :param _port: 端口号
    :param _host: 主机名
    :return: True/False
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((_host, _port))
        return True
    except OSError:
        return False
    finally:
        if s:
            s.close()


def get_self_ip() -> str:
    """获取自身ip

    https://www.zhihu.com/question/49036683/answer/124321702
    """
    s = None
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        if s:
            s.close()


def copy_property(dict_: dict, obj: object) -> None:
    """复制属性，将dict中出现并且对象属性中存在同名的进行拷贝

    :param dict_: 来源字典
    :param obj: 目标对象
    :return: None
    """
    # TODO: 这里只能转换一层...
    for key, value in dict_.items():
        if hasattr(obj, key):
            setattr(obj, key, value)


T = TypeVar('T')


def dict_to_object(dict_: dict, class_: T) -> Type[T]:
    """将字典转换为类实例

    :param dict_: 字典
    :param class_: 类
    :return: 对象
    """
    obj = class_()
    copy_property(dict_, obj)
    return obj


def get_os_type() -> OSType:
    """获取系统类型"""
    system = platform.system().strip().lower()
    arch = platform.machine().strip().lower()
    if system.startswith('win'):
        if arch.startswith('amd64') or arch.startswith('x86_64'):
            return OSType.WINDOWS_AMD64
    elif system.startswith('lin'):
        if arch.startswith('amd64') or arch.startswith('x86_64'):
            return OSType.LINUX_AMD64
    raise TypeError(f'Unknown system: {system} {arch}')


def os_type_to_asset_finder(type_: OSType) -> Pattern[AnyStr]:
    """获取系统类型对应的 go-cqhttp 发行版正则匹配器"""
    if type_ == OSType.WINDOWS_AMD64:
        return re.compile(r'win.+amd64.*\.zip')  # type: ignore[arg-type]
    elif type_ == OSType.WINDOWS_I386:
        return re.compile(r'win.+386.*\.zip')  # type: ignore[arg-type]
    elif type_ == OSType.LINUX_AMD64:
        return re.compile(r'linux.+amd64.*tar\.gz')  # type: ignore[arg-type]
    elif type_ == OSType.LINUX_I386:
        return re.compile(r'linux.+386.*tar\.gz')  # type: ignore[arg-type]
    raise TypeError(f'Unknown system: {type_}')


def download_file(url: str, file_path: str) -> None:
    """下载文件并显示进度条

    :param url: 文件url
    :param file_path: 文件路径，需包含文件名，会覆盖已有文件
    """
    file = Path(file_path)
    if file.is_dir() or file.is_symlink():
        raise FileExistsError(f'{file_path} is a directory or a symbolic link')
    if file.exists():
        file.unlink()
    if file.exists():
        raise FileExistsError(f'{file_path} cannot be deleted')
    file.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, stream=True)
    tracker = track(
        r.iter_content(chunk_size=1024),
        description=f'[bold blue]{PurePath(file_path).name}',
        total=int(r.headers['Content-Length']) // 1024
    )
    with atomic_write(file_path, mode='wb') as f:
        for chunk in tracker:
            if chunk:
                f.write(chunk)


def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128) -> str:
    """计算校验和(不会全部读入内存)

    :param filename: 文件名
    :param hash_factory: 哈希算法
    :param chunk_num_blocks: 分块数
    """
    h = hash_factory()
    with open(filename, 'rb') as f:
        while chunk := f.read(chunk_num_blocks * h.block_size):
            h.update(chunk)
    return h.hexdigest()


def get_random_str(length: int) -> str:
    """生成数字+大小写随机字符串

    :param length: 长度
    """
    char_list = string.ascii_letters + string.digits
    return ''.join(random.choices(char_list, k=length))


def get_system_uptime() -> str:
    """获取系统运行时间

    :return: 系统运行时间 like: 24 days, 18:30:43
    """
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    curr_time = datetime.now()
    uptime = curr_time - boot_time
    return str(uptime).split('.')[0]


def get_script_uptime() -> str:
    """获取脚本运行时间

    :return: 脚本运行时间 like: 24
    """
    self_process = psutil.Process(os.getpid())
    curr_time = datetime.now()
    start_time = self_process.create_time()
    start_time = datetime.fromtimestamp(start_time)
    uptime = curr_time - start_time
    return str(uptime).split('.')[0]


def get_system_memory_usage(round_: int = 4) -> float:
    """获取系统内存使用率

    :param round_: 保留小数位数
    """
    platform_memory = psutil.virtual_memory()
    platform_memory_usage = 1 - platform_memory.available / platform_memory.total
    platform_memory_usage *= 100
    return round(platform_memory_usage, round_)


def get_script_memory_usage(round_: int = 4) -> float:
    """获取脚本内存占用率

    :param round_: 保留小数位数
    """
    self_process = psutil.Process(os.getpid())
    return round(self_process.memory_percent(), round_)


def get_script_cpu_present(interval: float = 1) -> float:
    """获取脚本CPU占用率"""
    self_process = psutil.Process(os.getpid())
    return self_process.cpu_percent(interval)


def get_system_description() -> str:
    """获取系统版本"""
    system = platform.system().strip().lower()
    if system.startswith('win'):
        platform_system = 'Windows'
        platform_version = platform.version()
    else:
        platform_system = distro.name(True)
        platform_version = ''
    return f'{platform_system} {platform_version} {platform.machine().strip()}'


def print_qrcode(text: str) -> None:
    """在控制台打印二维码"""
    qr = qrcode.QRCode()
    qr.add_data(text)
    with StringIO() as out:
        qr.print_ascii(out, invert=True)
        print(out.getvalue())


def decode_qrcode(file_data: bytes) -> str:
    """二维码解码"""
    with BytesIO() as bytes_io:
        bytes_io.write(file_data)
        with Image.open(bytes_io) as img:
            a = pyzbar_decode(img)
            b = a[0]
            c = b.data
            d = c.decode('utf-8')
            return d


def get_random_free_port(min_: int = 10000, max_: int = 65535, default: int = None) -> int:
    """获取一个随机空闲端口

    :param min_: 最小端口号
    :param max_: 最大端口号
    :param default: 默认端口号
    :return: 空闲端口号
    """
    if default and not is_port_in_use(default):
        return default

    result = random.randint(min_, max_)
    while is_port_in_use(result):
        result = random.randint(min_, max_)
    return result


def change_console_title(title: str) -> None:
    """Windows 平台修改控制台标题"""
    import contextlib
    import ctypes
    with contextlib.suppress(Exception):
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def kill_thread(thread: Thread) -> None:
    """强制结束线程，注意不得设计为对象方法！"""
    exctype = SystemExit
    if not (thread.is_alive() and thread.ident):
        return
    import ctypes
    tid = ctypes.c_long(thread.ident)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError('invalid thread id')
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')


if __name__ == '__main__':
    print(get_system_uptime())
    print(get_script_uptime())
    print(get_system_memory_usage())
    print(get_script_memory_usage())
    print(get_script_cpu_present())
    print(get_system_description())
