from assets.default_config import DEFAULT_GOCQ_CONFIG, DEFAULT_MIDDLEWARE
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
        self.config = YamlConfig(Global().gocq_config_path)
        if not self.config.data:
            self.create_default_config()

    def create_default_config(self) -> None:
        """创建默认配置"""
        self.config.cover(DEFAULT_GOCQ_CONFIG)
        self.config.save()

    def refresh(self) -> None:
        """刷新配置"""
        self.config.load()
        data = self.config.data
        servers: list = data['servers']
        servers.extend({} for _ in range(2 - len(servers)))
        servers[0]['http'] = {
            'address': '127.0.0.1:35700',
            'timeout': 5,
            'long-polling': {
                'enabled': False,
                'max-queue-size': 2000,
            },
            'middlewares': DEFAULT_MIDDLEWARE,
        }
        servers[1]['ws-reverse'] = {
            'universal': f'ws://127.0.0.1:{Global().user_config.port}/instance',
            'reconnect-interval': 3000,
            'middlewares': DEFAULT_MIDDLEWARE,
        }
        self.config.cover(data)
        self.config.save()
