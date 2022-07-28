from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType

HELP_TEXT = """Available commands:
/help: Show this help message
/exit: Quit the application
"""


class CommandHandler(metaclass=SingletonType):
    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)

    def add(self, command) -> None:
        self.log.debug(f'Add command: {command}')
        if command in ['/help', '/h']:
            Global().console.print(HELP_TEXT)
        elif command == '/exit':
            Global().time_to_exit = True
        else:
            self.log.error('Invalid Command')
