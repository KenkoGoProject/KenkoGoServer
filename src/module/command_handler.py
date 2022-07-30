from fastapi import WebSocket
from rich.table import Table

from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType
from module.utils import decode_qrcode, print_qrcode

HELP_TEXT = """支持的命令 Available commands:
/help: 显示此帮助 Show this help message
/exit: 退出KenkoGo Quit the application

/info: 查看各种信息 Show the information

/start: 启动go-cqhttp Start go-cqhttp
/stop: 停止go-cqhttp Stop go-cqhttp
/qrcode: 显示登录二维码 Show qrcode of go-cqhttp

/list：列出所有客户端 List all clients
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
        elif command in ['/qrcode', '/qr']:
            try:
                with Global().qrcode_path.open('rb') as f:
                    qrcode = f.read()
                code_url = decode_qrcode(qrcode)
                print_qrcode(code_url)
            except Exception as e:
                self.log.error(e)
        elif command in ['/list', '/ls', 'ls']:
            self.list_clients()
        else:
            self.log.error('Invalid Command')

    @staticmethod
    def list_clients() -> None:
        table = Table(title='客户端 Clients')
        table.add_column('地址 Address', style='deep_sky_blue1')

        websockets = Global().websocket_manager.active_connections
        for websocket in websockets:
            websocket: WebSocket = websocket[0]
            client = websocket.client
            table.add_row(f'{client.host}:{client.port}')

        Global().console.print(table)
