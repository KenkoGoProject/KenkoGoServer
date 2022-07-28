from assets.default_config import DEFAULT_GOCQ_CONFIG
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType
from module.yaml_config import YamlConfig


class GocqConfig(metaclass=SingletonType):
    """go-cqhttp config"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.data = YamlConfig(Global().gocq_config_path)

    def create_default_config(self) -> None:
        """创建默认配置"""
        self.data.update(DEFAULT_GOCQ_CONFIG)
        self.data.save()

    # TODO: 增加配置项的检查
