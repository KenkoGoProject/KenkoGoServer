from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType

HELP_TEXT = """支持的命令 Available commands:
/help: 显示此帮助 Show this help message
/exit: 退出KenkoGo Quit the application

/info: 查看各种信息 Show the information

/start: 启动go-cqhttp Start go-cqhttp
/stop: 停止go-cqhttp Stop go-cqhttp
===Below are the commands working in progress===
/qrcode: 显示登录二维码 Show qrcode of go-cqhttp

/list：列出所有客户端 List all clients
/kick: 踢出所有客户端 Kick all clients
"""


class CommandHandler(metaclass=SingletonType):
    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)

    def add(self, command) -> None:
        self.log.debug(f'Get command: {command}')
        if command in ['/help', '/h']:
            Global().console.print(HELP_TEXT)
        elif command == '/exit':
            Global().time_to_exit = True
        elif command == '/info':
            Global().console.print_object(Global().information)
        elif command == '/start':
            Global().instance_manager.start()
        elif command == '/stop':
            Global().instance_manager.stop()
        else:
            self.log.error('Invalid Command')
