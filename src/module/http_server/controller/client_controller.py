import hashlib
from pathlib import Path, PurePath

import requests
from fastapi import (APIRouter, Request, UploadFile, WebSocket,
                     WebSocketDisconnect)

from module.global_dict import Global
from module.http_server.http_result import HttpResult
from module.logger_ex import LoggerEx, LogLevel
from module.utils import get_random_str


class ClientController(APIRouter):
    """客户端接口"""

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
            'Authorization': 'Bearer 1231',  # 鉴权
            'Content-Type': 'application/json',
        })
        self.websocket_manager = Global().websocket_manager

        self.add_api_websocket_route('', self.client_websocket)
        self.add_api_route('/api/{api_name}', self.gocq_api_proxy, methods=['GET', 'POST'])
        self.add_api_route('/upload', self.upload_file, methods=['POST'])

    async def client_websocket(self, ws: WebSocket, blob: bool = False) -> None:
        """客户端WebSocket"""
        await self.websocket_manager.connect(ws, blob)
        client = ws.client
        try:
            while True:
                call_func = ws.receive_bytes if blob else ws.receive_text
                s = await call_func()
                self.ws_log.debug(f'{client.host}:{client.port} < {s[:200]}')
        except WebSocketDisconnect:
            self.websocket_manager.disconnect(ws)
        except Exception as e:
            self.ws_log.error(f'{ws.client} : {e}')

    async def gocq_api_proxy(self, api_name: str, request: Request) -> dict:
        """go-cqhttp API转发"""
        base_url = f'http://127.0.0.1:{Global().gocq_config.api_port}'
        body = await request.body()
        method = request.method
        self.log.debug(f'{method:.4s} {base_url}/{api_name} {body[:200]} {self.r.headers}')
        try:
            response = self.r.request(method, f'{base_url}/{api_name}', data=body)
        except Exception as e:
            self.log.error(f'{e}')
            return HttpResult.error(f'{e}')
        self.log.debug(f'{response.status_code} {response.text}')
        return response.json()

    async def upload_file(self, file: UploadFile, _: Request):
        """上传文件到服务器"""
        file_type = PurePath(file.filename).suffix[1:].lower()
        local_file = Path(Global().download_dir, get_random_str(20))
        h = hashlib.md5()
        file.file.seek(0)
        with local_file.open('wb') as real_file:
            while chunk := file.file.read(128 * h.block_size):
                h.update(chunk)  # 对数据进行hash
                real_file.write(chunk)  # 写入文件
        md5 = h.hexdigest()
        r = {
            'name': file.filename,
            'type': file_type,
            'size': file.file.tell(),
            'md5': md5,
        }
        await file.close()
        self.log.debug(f'{r}')
        new_name = Path(Global().download_dir, md5)
        new_name = new_name.with_suffix(f'.{file_type}')
        if not new_name.exists():
            new_name.unlink(missing_ok=True)
        local_file.rename(new_name)
        r['path'] = str(new_name)
        return HttpResult.success(r)
