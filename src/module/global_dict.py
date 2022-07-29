from pathlib import Path
from typing import Optional

from assets.os_type import OSType
from module.console import Console
from module.singleton_type import SingletonType
from module.utils import get_os_type, get_self_ip


class Global(metaclass=SingletonType):
    """单例模式，全局变量"""

    ############
    # 基础的信息 #
    ############

    app_name = 'KenkoGo'  # 应用名称
    author_name = 'AkagiYui'  # 作者
    version_num = 11  # 版本号
    version_str = '0.2.0'  # 版本名称
    description = 'A Controller of go-cqhttp'  # 描述

    ############
    # 全局的变量 #
    ############

    exit_code = 0  # 退出码
    time_to_exit = False  # 是时候退出了
    debug_mode = False  # 调试模式

    info_receive_from_gocq_count = 0  # 接收到的信息数量

    @property
    def information(self) -> dict:
        """获取应用信息"""
        return {
            'gocq_msg_count': self.info_receive_from_gocq_count,
        }

    @property
    def host_with_port(self) -> Optional[str]:  # host:port
        if not self.user_config:
            return None
        host = self.user_config.host
        if host not in ('localhost', '127.0.0.1'):
            host = get_self_ip()
        return f'{host}:{self.user_config.port}'

    ############
    # 共享的对象 #
    ############

    user_config = None  # 用户配置  # type: UserConfig
    console: Console = None  # 控制台对象
    command_handler = None  # 命令处理器  # type: CommandHandler
    kenko_go = None  # 应用程序  # type: KenkoGo
    gocq_config = None  # go-cqhttp 配置文件 # GocqConfig
    websocket_manager = None  # WebSocketManager
    gocq_binary_manager = None  # go-cqhttp 二进制文件管理器
    gocq_instance_manager = None  # GocqInstanceManager

    args_known = ()  # 命令行参数
    args_unknown = ()  # 未知命令

    ############
    # 目录与路径 #
    ############

    root_dir = Path('.')  # 根目录
    download_dir = Path(root_dir, 'downloads')  # 下载目录

    gocq_dir = Path(root_dir, 'gocq')  # gocq实例目录
    gocq_config_path = Path(gocq_dir, 'config.yml')  # gocq配置文件路径
    qrcode_path = Path(gocq_dir, 'qrcode.png')  # 二维码路径

    def __init__(self):
        for dir_ in [self.download_dir, self.gocq_dir]:
            dir_.mkdir(parents=True, exist_ok=True)

        os_type = get_os_type()
        if os_type in [OSType.WINDOWS_AMD64, OSType.WINDOWS_I386]:
            self.gocq_binary_name = 'go-cqhttp.exe'  # Windows go-cqhttp 二进制文件名
        elif os_type in [OSType.LINUX_AMD64, OSType.LINUX_I386]:
            self.gocq_binary_name = 'go-cqhttp'  # Linux go-cqhttp 二进制文件名
        else:
            raise TypeError(f'Unsupported OS type: {os_type}')

        self.gocq_path = Path(self.gocq_dir, self.gocq_binary_name)  # go-cqhttp 可执行文件路径


if __name__ == '__main__':
    print(Global().debug_mode)
