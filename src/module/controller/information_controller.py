from fastapi import APIRouter

from assets.http_result import HttpResult
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel


class InformationController(APIRouter):
    # TODO: 此处应使用单例模式

    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/info', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.add_api_route('', self.overview, methods=['GET'])

    @staticmethod
    async def overview() -> dict:
        """数据概览"""
        return HttpResult.success(Global().information)
