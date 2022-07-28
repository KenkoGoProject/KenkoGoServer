from fastapi import APIRouter

from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel


class GocqEventController(APIRouter):
    # TODO: 此处应使用单例模式
    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/gocqevent', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')
