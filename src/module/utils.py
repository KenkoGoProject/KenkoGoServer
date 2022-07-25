import hashlib
import hmac
import platform
import random
import re
import socket
import tarfile
import zipfile
from pathlib import Path, PurePath
from re import Pattern
from typing import AnyStr

import requests
from rich.progress import track

from assets.os_type import OSType
from module.atomicwrites import atomic_write
from module.exception_ex import UnknownSystemError


def is_port_in_use(_port: int, _host='127.0.0.1'):
    """检查端口是否被占用"""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((_host, _port))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()


def get_random_free_port():
    """获取一个随机空闲端口"""
    result = random.randint(10000, 65535)
    while is_port_in_use(result):
        result = random.randint(10000, 65535)
    return result


def get_self_ip():
    """获取自身ip
    https://www.zhihu.com/question/49036683/answer/1243217025
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


def get_public_ip(method: int = 0):
    """获取公网ip"""
    if method == 0:
        return requests.get('https://api.ipify.org').text
    elif method == 1:
        return requests.get('https://api.ip.sb/ip').text
    elif method == 2:
        return requests.get('http://myexternalip.com/raw').text
    elif method == 3:
        return requests.get('http://ip.42.pl/raw').text
    elif method == 4:
        return requests.get('http://myip.ipip.net/').text  # 非纯ip
    elif method == 5:
        return requests.get('http://ipecho.net/plain').text
    elif method == 6:
        return requests.get('http://hfsservice.rejetto.com/ip.php').text


def hash_mac(key: str, content: bytes, alg=hashlib.sha1):
    """hash mac"""
    hmac_code = hmac.new(key.encode(), content, alg)
    return hmac_code.hexdigest()


def copy_property(dict_: dict, obj: object):
    """copy property"""
    # TODO: 这里只能转换一层...
    for key, value in dict_.items():
        if hasattr(obj, key):
            setattr(obj, key, value)


def dict_to_object(dict_: dict, class_: type):
    """dict to class"""
    obj = class_()
    copy_property(dict_, obj)
    return obj


def get_os_type() -> OSType:
    system = platform.system().strip().lower()
    arch = platform.machine().strip().lower()
    if system.startswith('win'):
        if arch.startswith('amd64') or arch.startswith('x86_64'):
            return OSType.WINDOWS_AMD64
    elif system.startswith('lin'):
        if arch.startswith('amd64') or arch.startswith('x86_64'):
            return OSType.LINUX_AMD64
    raise UnknownSystemError(f'Unknown system: {system} {arch}')


def os_type_to_asset_finder(type_: OSType) -> Pattern[AnyStr]:
    if type_ == OSType.WINDOWS_AMD64:
        return re.compile(r'win.+amd64.*\.zip')  # type: ignore[arg-type]
    elif type_ == OSType.WINDOWS_I386:
        return re.compile(r'win.+386.*\.zip')  # type: ignore[arg-type]
    elif type_ == OSType.LINUX_AMD64:
        return re.compile(r'linux.+amd64.*tar\.gz')  # type: ignore[arg-type]
    elif type_ == OSType.LINUX_I386:
        return re.compile(r'linux.+386.*tar\.gz')  # type: ignore[arg-type]
    raise UnknownSystemError(f'Unknown system: {type_}')


def download_file(url: str, file_path: str):
    """下载文件"""
    file = Path(file_path)
    if file.is_dir() or file.is_symlink():
        raise FileExistsError(f'{file_path} is a directory or a symbolic link')
    if file.exists():
        file.unlink()
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


def decompress_file(file_path: str, decompress_path: str):
    """解压文件"""
    file = Path(file_path)
    if file.is_dir() or file.is_symlink():
        raise FileExistsError(f'{file_path} is a directory or a symbolic link')
    Path('.', 'assets', 'gocq').mkdir(parents=True, exist_ok=True)
    if file.suffix == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(decompress_path)
    elif file.suffix == '.tar.gz':
        with tarfile.open(file_path, 'r:gz') as tar_file:
            tar_file.extractall(decompress_path)
    else:
        raise ValueError(f'Unknown file suffix: {file.suffix}')
