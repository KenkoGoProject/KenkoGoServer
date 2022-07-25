from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from assets.http_result import HttpResult
from module.controller.websocket_manager import WebsocketManager
from module.global_dict import Global
from module.gocq_instance import GocqInstance
from module.logger_ex import LoggerEx, LogLevel


class InstanceController(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/instance', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.ws_log = LoggerEx('WebSocket')
        if Global().debug_mode:
            self.ws_log.set_level(LogLevel.DEBUG)

        self.instance = GocqInstance()
        self.websocket_manager = WebsocketManager()

        self.add_api_route('/check', self.check, methods=['POST'])
        self.add_api_route('/start', self.start, methods=['POST'])
        self.add_api_route('/stop', self.stop, methods=['POST'])
        self.add_api_route('/qrcode', self.qrcode, methods=['GET'])
        self.add_api_websocket_route('', self.gocq_websocket)
        self.add_api_websocket_route('/client', self.client_websocket)

    async def client_websocket(self, ws: WebSocket, text: bool = False):
        await self.websocket_manager.connect(ws, text)
        client = ws.client
        try:
            while True:
                s = await ws.receive_text()
                self.ws_log.debug(f'{client.host}:{client.port} < {s}')
        except WebSocketDisconnect:
            await self.websocket_manager.disconnect(ws)
        except Exception as e:
            self.ws_log.error(f'{ws.client} : {e}')

    async def gocq_websocket(self, ws: WebSocket):
        await ws.accept()
        client = ws.client
        self.ws_log.info(f'New gocq connection: {client.host}:{client.port}')
        try:
            while True:
                s = await ws.receive_text()
                self.ws_log.debug(f'{client.host}:{client.port} < {s}')
                await self.websocket_manager.broadcast(s)
        except WebSocketDisconnect:
            self.ws_log.info(f'Gocq connection closed: {client.host}:{client.port}')
        except Exception as e:
            self.ws_log.error(f'{client} : {e}')

    async def check(self):
        return HttpResult.success(self.instance.check())

    async def start(self):
        return HttpResult.success(self.instance.start())

    async def stop(self):
        return HttpResult.success(self.instance.stop())

    async def qrcode(self):
        if Global().qrcode_path.is_file():
            return FileResponse(Global().qrcode_path)
        else:
            return HttpResult.not_found()
