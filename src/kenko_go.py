import uvicorn as uvicorn

from module.exception_ex import PortInUseException
from module.global_dict import Global
from module.http_server.http_server import HttpServer
from module.logger_ex import LoggerEx, LogLevel
from module.server_status import ServerStatus
from module.thread_ex import ThreadEx
from module.utils import Utils


class KenkoGo:
    VERSION: int = 8  # 版本号
    VERSION_STRING: str = '0.1.1'  # 版本名称
    APP_NAME: str = 'KenkoGo - Server'  # 应用名称

    _status: ServerStatus = ServerStatus.STOPPED

    def __init__(self):
        self.log = LoggerEx('KenkoGo')
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.http_thread = None

        # 打印版本信息
        self.log.info(self.APP_NAME)
        self.log.info(f'Version: {self.VERSION_STRING}')
        self.log.debug(f'Version Num: {self.VERSION}')

    def start(self):
        if Utils.is_port_in_use(Global().user_config.port):
            raise PortInUseException(f'Port {Global().user_config.port} already in use')
        self.http_thread = ThreadEx(
            target=uvicorn.run,
            daemon=True,
            kwargs={
                'app': HttpServer(),
                'host': Global().user_config.host,
                'port': Global().user_config.port,
                'log_level': 'error' if Global().debug_mode else 'critical',
            }
        )
        self.http_thread.start()
        self._status = ServerStatus.HTTP_THREAD_STARTED
        self.log.info(f'KenkoGo Started at http://{Global().user_config.host}:{Global().user_config.port} .')

    def stop(self):
        self.log.debug('KenkoGo Stopping.')
        if self._status != ServerStatus.STOPPED and isinstance(self.http_thread, ThreadEx):
            # TODO: 实现优雅的关闭
            self.http_thread.kill()
            self._status = ServerStatus.STOPPED
