from fastapi import APIRouter

from assets.http_result import HttpResult
from module.exception_ex import ReleaseNotFoundError
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel


class GocqBinaryController(APIRouter):
    """go-cqhttp 二进制文件操作接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/binary', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')
        self.gocq_binary_manager = Global().gocq_binary_manager

        self.add_api_route('/remoteversion', self.get_remote_version, methods=['GET'])
        self.add_api_route('/download', self.download_remote_version, methods=['POST'])

    async def get_remote_version(self, use_cache: bool = True) -> dict:
        """获取远端发行版列表"""
        return HttpResult.success(self.gocq_binary_manager.get_remote_release(use_cache))

    async def download_remote_version(self, version: str = None) -> dict:
        """下载远端发行版"""
        try:
            self.gocq_binary_manager.download_remote_version(version)
        except ReleaseNotFoundError:
            return HttpResult.not_found('Release not found.')
        return HttpResult.success()
