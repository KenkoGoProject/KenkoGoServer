from fastapi import WebSocket
from rich.table import Table

from module.common.logger_ex import LoggerEx, LogLevel
from module.common.singleton_type import SingletonType
from module.constans import COMMAND_HELP_TEXT
from module.global_dict import Global


class CommandHandler(metaclass=SingletonType):
    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)

    def add(self, command) -> None:
        self.log.debug(f'Get command: {command}')
        if command in ['/help', '/h']:
            Global().console.print(COMMAND_HELP_TEXT)
        elif command == '/exit':
            Global().time_to_exit = True
        elif command == '/info':
            Global().console.print_object(Global().information)
        elif command == '/start':
            Global().instance_manager.start()
        elif command == '/stop':
            Global().instance_manager.stop()
        elif command in ['/qrcode', '/qr']:
            qrcode_path = Global().qrcode_path
            if qrcode_path.exists():
                try:
                    # with Global().qrcode_path.open('rb') as f:
                    #     qrcode = f.read()
                    # code_url = decode_qrcode(qrcode)
                    # print_qrcode(code_url)
                    ...
                except Exception as e:
                    self.log.error(e)
            else:
                self.log.error('qrcode not exists')
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
