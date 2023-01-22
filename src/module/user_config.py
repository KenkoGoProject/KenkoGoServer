from module.common.logger_ex import LoggerEx, LogLevel
from module.common.singleton_type import SingletonType
from module.common.yaml_config import YamlConfig
from module.global_dict import Global


class UserConfig(metaclass=SingletonType):
    host = '0.0.0.0'  # 监听地址
    port = 18082  # 监听端口
    token = ''  # http token
    github_proxy = ''  # GitHub代理配置

    data: YamlConfig = {}

    def __init__(self, file_path):
        self.log = LoggerEx(self.__class__.__name__)
        self.file_path = file_path
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.load()

    def load(self) -> None:
        self.log.debug(f'Loading config file: {self.file_path}')
        self.data = YamlConfig(self.file_path)
        need_save = len(self.data) == 0

        # 读取配置
        self.port = int(self.data.get('port', self.port))
        self.host = str(self.data.get('host', self.host))
        self.token = str(self.data.get('token', self.token))
        self.github_proxy = str(self.data.get('github_proxy', self.github_proxy))

        # 若配置项不存在，则创建配置项
        self.data.setdefault('port', self.port)
        self.data.setdefault('host', self.host)
        self.data.setdefault('token', self.token)
        self.data.setdefault('github_proxy', self.github_proxy)

        self.log.debug(f'Config loaded: {dict(self.data)}')
        if need_save:
            self.save()

    def save(self) -> None:
        self.log.debug(f'Saving config file: {self.file_path}')
        self.data.save()  # TODO: 写出时保留注释
        self.log.debug(f'Config saved: {dict(self.data)}')
