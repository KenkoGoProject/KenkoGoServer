from assets.default_config import default_gocq_config
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType
from module.yaml_config import YamlConfig


class GocqConfig(metaclass=SingletonType):
    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.data = YamlConfig(Global().gocq_config_path)

    def create_default_config(self):
        self.data.update(default_gocq_config)
        self.data.save()
