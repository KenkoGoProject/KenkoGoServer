from fastapi import APIRouter

from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel


class InstanceController(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/gocqbin', *args, **kwargs)
        self.log = LoggerEx('GocqBinController')
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug('InstanceController Initializing...')
