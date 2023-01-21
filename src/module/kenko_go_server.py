from threading import Thread

import uvicorn as uvicorn

from module.constans import APP_DESCRIPTION, APP_NAME, VERSION_NUM, VERSION_STR
from module.exception_ex import PortInUseError
from module.global_dict import Global
from module.gocq_binary_manager import GocqBinaryManager
from module.gocq_config import GocqConfig
from module.http_server.http_server import HttpServer
from module.instance_manager import InstanceManager
from module.logger_ex import LoggerEx, LogLevel
from module.user_config import UserConfig
from module.utils import is_port_in_use, kill_thread
from module.websocket_manager import WebsocketManager


class KenkoGoServer:
    """主功能模块"""

    def __init__(self, _: UserConfig):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        # 一定要严格按照顺序初始化，否则可能会出现异常
        Global().gocq_config = GocqConfig()
        Global().websocket_manager = WebsocketManager()
        Global().instance_manager = InstanceManager()
        Global().gocq_binary_manager = GocqBinaryManager()
        self.http_app = HttpServer()
        self.http_thread = None

        # 打印版本信息
        self.log.info(f'{APP_NAME} - {APP_DESCRIPTION}')
        self.log.info(f'Version: {VERSION_STR}')
        self.log.debug(f'Version Num: {VERSION_NUM}')

    def start(self) -> None:
        """启动KenkoGoServer"""
        if is_port_in_use(Global().user_config.port):  # 检查端口是否被占用
            raise PortInUseError(f'Port {Global().user_config.port} already in use')
        self.start_asgi()

    def stop(self) -> None:
        """停止KenkoGoServer"""
        self.log.debug(f'{APP_NAME} stopping.')
        self.stop_asgi()
        self.log.info(f'{APP_NAME} stopped, see you next time.')

    def start_asgi(self) -> None:
        """启动ASGI"""
        self.log.debug(f'{APP_NAME} starting ASGI.')
        self.http_thread = Thread(
            target=uvicorn.run,
            daemon=True,
            kwargs={
                'app': self.http_app,
                'host': Global().user_config.host,
                'port': Global().user_config.port,
                'log_level': 'warning' if Global().debug_mode else 'critical',
            }
        )
        self.http_thread.start()

    def stop_asgi(self) -> None:
        """停止ASGI"""
        self.log.debug(f'{APP_NAME} stopping ASGI.')
        if isinstance(self.http_thread, Thread) and self.http_thread.is_alive():
            # self.websocket_manager.broadcast('stop')
            kill_thread(self.http_thread)   # TODO: 实现优雅的关闭
            # print(1, self.http_thread.is_alive())
            # signal.pthread_kill(self.http_thread.ident, signal.SIGINT)
            # time.sleep(1)
            # print(2, self.http_thread.is_alive())
