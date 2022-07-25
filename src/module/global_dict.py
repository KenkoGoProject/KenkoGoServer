from pathlib import Path
from typing import Any

from assets.os_type import OSType
from module.console import Console
from module.singleton_type import SingletonType
from module.utils import get_os_type, get_self_ip


class Global(metaclass=SingletonType):
    """单例模式，全局变量"""
    _members: dict[str, Any] = {}
    __dict__ = _members

    app_name = 'KenkoGo'  # 应用名称
    author_name = 'AkagiYui'  # 作者
    version_num = 9  # 版本号
    version_str = '0.1.3'  # 版本名称
    description = 'A Controller of go-cqhttp'  # 描述

    exit_code = 0  # 退出码
    time_to_exit = False  # 是时候退出了

    debug_mode = False  # 调试模式
    command: str = ''  # 命令
    user_config = None  # 用户配置  # type: UserConfig
    console: Console = None  # 控制台对象

    args_known = ()  # 命令行参数
    args_unknown = ()  # 未知命令

    #######
    # 路径 #
    #######

    root_dir = Path('.')  # 根目录
    asset_dir = Path(root_dir, 'assets')  # 静态资源目录
    download_dir = Path(asset_dir, 'downloads')  # 下载目录

    gocq_asset_dir = Path(asset_dir, 'gocq')  # gocq 资源目录

    gocq_dir = Path(root_dir, 'gocq')  # gocq实例目录
    gocq_config_path = Path(gocq_dir, 'config.yml')  # gocq配置文件路径
    qrcode_path = Path(gocq_dir, 'qrcode.png')  # 二维码路径

    def __init__(self):
        for dir_ in [self.asset_dir, self.download_dir, self.gocq_asset_dir, self.gocq_dir]:
            dir_.mkdir(parents=True, exist_ok=True)

        os_type = get_os_type()
        if os_type in [OSType.WINDOWS_AMD64, OSType.WINDOWS_I386]:
            self.gocq_bin_name = 'go-cqhttp.exe'
        elif os_type in [OSType.LINUX_AMD64, OSType.LINUX_I386]:
            self.gocq_bin_name = 'go-cqhttp'
        else:
            raise TypeError(f'Unsupported OS type: {os_type}')

        self.gocq_path = Path(self.gocq_dir, self.gocq_bin_name)
        self.gocq_bin_path = Path(self.gocq_asset_dir, self.gocq_bin_name)

    @property
    def host_with_port(self):
        if not self.user_config:
            return None
        host = self.user_config.host
        if host not in ('localhost', '127.0.0.1'):
            host = get_self_ip()
        return f'{host}:{self.user_config.port}'

    # def __setattr__(self, key, value):
    #     self._members[key] = value
    #
    # def __getattr__(self, key):
    #     try:
    #         return self._members[key]
    #     except KeyError:
    #         return None
    #
    # def __delattr__(self, key):
    #     del self._members[key]

    def __repr__(self):
        return self._members.__repr__()

    def __getitem__(self, item):
        return self._members[item]

    def __setitem__(self, key, value):
        self._members[key] = value

    def __delitem__(self, key):
        del self._members[key]

    def __iter__(self):
        return iter(self._members)

    def items(self):
        return self._members.items()

    def keys(self):
        return self._members.keys()

    def values(self):
        return self._members.values()

    def clear(self):
        self._members.clear()


if __name__ == '__main__':
    for k, v in Global().items():
        print(k, v)

    Global().debug_mode = True
    print(Global().debug_mode)
