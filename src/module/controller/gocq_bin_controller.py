from fastapi import APIRouter

from assets.http_result import HttpResult
from module.exception_ex import ReleaseNotFoundError
from module.global_dict import Global
from module.gocq_bin import GocqBin
from module.logger_ex import LoggerEx, LogLevel


class GocqBinController(APIRouter):
    # TODO: 此处应使用单例模式
    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/gocqbin', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')
        self.gocq_bin = GocqBin()

        self.add_api_route('/remoteversion', self.get_remote_version, methods=['GET'])
        self.add_api_route('/download', self.download_remote_version, methods=['POST'])

    async def get_remote_version(self, use_cache: bool = True):
        return HttpResult.success(self.gocq_bin.get_remote_release(use_cache))

    async def download_remote_version(self, version: str = None):
        try:
            self.gocq_bin.download_remote_version(version)
        except ReleaseNotFoundError:
            return HttpResult.not_found('Release not found.')
        return HttpResult.success()
