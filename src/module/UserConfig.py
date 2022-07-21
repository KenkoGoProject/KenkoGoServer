from module.Global import Global
from module.LoggerEx import LoggerEx, LogLevel
from module.YamlConfig import YamlConfig


class UserConfig:
    host = '0.0.0.0'  # 监听地址
    port = 18082  # 监听端口

    data = None

    def __init__(self, file_path):
        self.log = LoggerEx('UserConfig')
        self.file_path = file_path
        if Global.debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.load()

    def load(self):
        self.log.debug(f'Loading config file: {self.file_path}')
        self.data = YamlConfig(self.file_path)
        self.port = self.data['port']
        self.host = self.data['host']
        self.log.debug(f'Config loaded: {dict(self.data)}')

    def save(self):
        self.log.debug(f'Saving config file: {self.file_path}')
        self.data.save()
        self.log.debug(f'Config saved: {dict(self.data)}')

