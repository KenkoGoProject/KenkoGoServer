import asyncio
import contextlib
import json
from typing import List, Tuple, Union

from fastapi import WebSocket

from module.global_dict import Global
from module.json_encoder_ex import JsonEncoderEx
from module.logger_ex import LoggerEx, LogLevel


# WebSocket连接管理器
class WebsocketManager:

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.active_connections: List[Tuple[WebSocket, bool]] = []

    async def connect(self, websocket: WebSocket, text: bool = False):
        await websocket.accept()
        client = websocket.client
        self.log.info(f'New client connection: {client.host}:{client.port}')
        connection = (websocket, text)
        self.active_connections.append(connection)
        await self.send_message(connection, 'Welcome!'.encode('utf-8'))

    def disconnect(self, websocket: WebSocket):
        client = websocket.client
        self.log.info(f'Client connection closed: {client.host}:{client.port}')
        for connection in self.active_connections:
            if connection[0] == websocket:
                self.active_connections.remove(connection)

    async def send_message(self, connection: Tuple[WebSocket, bool], message: Union[str, bytes, dict]):
        if isinstance(message, str):
            message = message.encode('utf-8')
        elif isinstance(message, dict):
            message = json.dumps(message, cls=JsonEncoderEx).encode('utf-8')
        if connection[1]:
            send_func = connection[0].send_text
            message = message.decode('utf-8')
        else:
            send_func = connection[0].send_bytes
        await send_func(message)

    async def broadcast(self, message: Union[str, bytes, dict]):
        for connection in self.active_connections:
            await self.send_message(connection, message)

    # def broadcast_sync(self, message: Union[str, bytes, dict]):
    #     try:
    #         loop = asyncio.get_running_loop()
    #         loop = loop.create_task
    #     except RuntimeError:
    #         loop = asyncio.new_event_loop()
    #         loop = loop.run_until_complete
    #     loop(self.broadcast(message))

    def close_all(self):  # 未实现
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        for connection in self.active_connections:
            with contextlib.suppress(ValueError):
                loop.run_until_complete(connection[0].close())
