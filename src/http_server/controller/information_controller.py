from fastapi import APIRouter

from common.http_result import HttpResult
from common.logger_ex import LoggerEx, LogLevel
from module.global_dict import Global


class InformationController(APIRouter):
    """信息接口"""

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
