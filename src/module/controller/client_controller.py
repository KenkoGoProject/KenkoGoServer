import hashlib
from pathlib import Path

import requests
from fastapi import (APIRouter, Request, UploadFile, WebSocket,
                     WebSocketDisconnect)

from assets.http_result import HttpResult
from module.controller.websocket_manager import WebsocketManager
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.utils import get_random_str


class ClientController(APIRouter):
    # TODO: 此处应使用单例模式
    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/client', *args, **kwargs)
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.ws_log = LoggerEx('ClientWebSocket')
        if Global().debug_mode:
            self.ws_log.set_level(LogLevel.DEBUG)

        self.r = requests.Session()
        self.r.headers.update({
            'Authorization': 'Bearer 1231',
            'Content-Type': 'application/json',
        })
        self.base_url = 'http://127.0.0.1:35700'
        self.websocket_manager = WebsocketManager()

        self.add_api_websocket_route('', self.client_websocket)
        self.add_api_route('/api/{api_name}', self.gocq_proxy, methods=['GET', 'POST'])
        self.add_api_route('/upload', self.upload_file, methods=['POST'])

    async def client_websocket(self, ws: WebSocket, blob: bool = False):
        await self.websocket_manager.connect(ws, blob)
        client = ws.client
        try:
            while True:
                s = await ws.receive_text()
                self.ws_log.debug(f'{client.host}:{client.port} < {s}')
        except WebSocketDisconnect:
            self.websocket_manager.disconnect(ws)
        except Exception as e:
            self.ws_log.error(f'{ws.client} : {e}')

    async def gocq_proxy(self, api_name: str, request: Request):
        body = await request.body()
        method = request.method
        call_func = self.r.get if method == 'GET' else self.r.post
        self.log.debug(f'{method:.4s} {self.base_url}/{api_name} {body[:200]} {self.r.headers}')
        try:
            response = call_func(f'{self.base_url}/{api_name}', data=body)
        except Exception as e:
            self.log.error(f'{e}')
            return HttpResult.error(f'{e}')
        self.log.debug(f'{response.status_code} {response.text}')
        return HttpResult.success(response.json())

    async def upload_file(self, file: UploadFile, request: Request):
        file.file.seek(0)
        h = hashlib.md5()
        with Path(Global().download_dir, get_random_str(20)).open('wb') as real_file:
            while chunk := file.file.read(128 * h.block_size):
                h.update(chunk)
                real_file.write(chunk)
        r = {
            'name': file.filename,
            'type': file.content_type,
            'size': file.file.tell(),
            'md5': h.hexdigest(),
        }
        await file.close()
        return HttpResult.success(r)
