import uvicorn as uvicorn

from module.exception_ex import PortInUseError
from module.global_dict import Global
from module.http_server import HttpServer
from module.logger_ex import LoggerEx, LogLevel
from module.thread_ex import ThreadEx
from module.utils import is_port_in_use


class KenkoGo:
    """主功能模块"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.http_thread = None

        # 打印版本信息
        self.log.info(f'{Global().app_name} - {Global().description}')
        self.log.info(f'Version: {Global().version_str}')
        self.log.debug(f'Version Num: {Global().version_num}')

    def start(self) -> None:
        """启动ASGI服务"""

        # 检查端口是否被占用
        if is_port_in_use(Global().user_config.port):
            raise PortInUseError(f'Port {Global().user_config.port} already in use')

        self.http_thread = ThreadEx(
            target=uvicorn.run,
            daemon=True,
            kwargs={
                'app': HttpServer(),
                'host': Global().user_config.host,
                'port': Global().user_config.port,
                'log_level': 'warning' if Global().debug_mode else 'critical',
            }
        )
        self.http_thread.start()

    def stop(self) -> None:
        """停止ASGI服务"""
        self.log.debug(f'{Global().app_name} stopping.')
        if isinstance(self.http_thread, ThreadEx) and self.http_thread.is_alive():
            self.http_thread.kill()  # TODO: 实现优雅的关闭
            # print(1, self.http_thread.is_alive())
            # signal.pthread_kill(self.http_thread.ident, signal.SIGINT)
            # time.sleep(1)
            # print(2, self.http_thread.is_alive())
        self.log.info(f'{Global().app_name} stopped, see you next time.')
