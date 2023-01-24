from typing import Union

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from common.http_result import HttpResult
from common.logger_ex import LoggerEx, LogLevel
from module.global_dict import Global


class InstanceController(APIRouter):
    """go-cqhttp 实例操作接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/instance', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.ws_log = LoggerEx('GocqWebSocket')
        if Global().debug_mode:
            self.ws_log.set_level(LogLevel.DEBUG)

        self.instance_manager = Global().instance_manager
        self.websocket_manager = Global().websocket_manager

        self.add_api_websocket_route('', self.gocq_websocket_proxy)
        self.add_api_route('/start', self.start, methods=['POST'])
        self.add_api_route('/stop', self.stop, methods=['POST'])
        self.add_api_route('/qrcode', self.qrcode, methods=['GET'], response_model=None)

    async def gocq_websocket_proxy(self, ws: WebSocket) -> None:
        """go-cqhttp WebSocket 转发代理"""
        await ws.accept()
        client = ws.client
        self.ws_log.info(f'New go-cqhttp connection: {client.host}:{client.port}')
        if 'authorization' in ws.headers:
            self.ws_log.debug(f'Connection token: {ws.headers["authorization"].removeprefix("Token ")}')
        try:
            while True:
                s = await ws.receive_text()
                self.ws_log.debug(f'{client.host}:{client.port} < {s}')
                Global().info_receive_from_gocq_count += 1
                await self.websocket_manager.broadcast(s)
        except WebSocketDisconnect:
            self.ws_log.info(f'go-cqhttp connection closed: {client.host}:{client.port}')
        except Exception as e:
            self.ws_log.error(f'{client} : {e}')

    async def start(self) -> dict:
        """启动实例"""
        if self.instance_manager.start():
            return HttpResult.success()
        else:
            return HttpResult.forbidden('Instance already started.')

    async def stop(self) -> dict:
        """停止实例"""
        if self.instance_manager.stop():
            return HttpResult.success()
        else:
            return HttpResult.forbidden('Instance already stopped.')

    async def qrcode(self) -> Union[FileResponse, dict]:
        """返回二维码图片"""
        if Global().qrcode_path.is_file():
            return FileResponse(Global().qrcode_path)
        else:
            return HttpResult.not_found()
