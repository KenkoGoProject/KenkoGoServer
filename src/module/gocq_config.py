from common.logger_ex import LoggerEx, LogLevel
from common.singleton_type import SingletonType
from common.utils import get_random_free_port
from common.yaml_config import YamlConfig
from module.default_config import DEFAULT_GOCQ_CONFIG, DEFAULT_MIDDLEWARE
from module.global_dict import Global


class GocqConfig(metaclass=SingletonType):
    """go-cqhttp config"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.config = YamlConfig(Global().gocq_config_path)
        if not self.config.data:
            self.create_default_config()
        self.api_port = self.get_api_port()

    def get_api_port(self) -> int:
        self.config.load()
        data = self.config.data
        try:
            servers: list = data['servers']
            address = servers[0]['http']['address']
        except KeyError:
            self.log.error('No http server configured')
            return 35700
        return int(address.split(':')[1])

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

        self.api_port = get_random_free_port(default=self.api_port)
        servers[0]['http'] = {
            'address': f'127.0.0.1:{self.api_port}',
            'timeout': 5,
            'long-polling': {
                'enabled': False,
                'max-queue-size': 2000,
            },
            'middlewares': DEFAULT_MIDDLEWARE.copy(),
        }
        servers[1]['ws-reverse'] = {
            'universal': f'ws://127.0.0.1:{Global().user_config.port}/instance',
            'reconnect-interval': 3000,
            'middlewares': DEFAULT_MIDDLEWARE.copy(),
        }
        self.config.cover(data)
        self.config.save()
