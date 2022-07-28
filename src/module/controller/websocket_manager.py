import asyncio
import contextlib
import json
from typing import List, Tuple, Union

from fastapi import WebSocket

from module.global_dict import Global
from module.json_encoder_ex import JsonEncoderEx
from module.logger_ex import LoggerEx, LogLevel
# WebSocket连接管理器
from module.singleton_type import SingletonType


class WebsocketManager(metaclass=SingletonType):

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.active_connections: List[Tuple[WebSocket, bool]] = []

    async def connect(self, websocket: WebSocket, blob: bool = False):
        await websocket.accept()
        client = websocket.client
        self.log.info(f'New client connection: {client.host}:{client.port}')
        connection = (websocket, blob)
        self.active_connections.append(connection)
        # await self.send_message(connection, 'Welcome!')

    def disconnect(self, websocket: WebSocket):
        client = websocket.client
        self.log.info(f'Client connection closed: {client.host}:{client.port}')
        for connection in self.active_connections:
            if connection[0] == websocket:
                self.active_connections.remove(connection)

    @staticmethod
    async def send_message(conn: Tuple[WebSocket, bool], message: Union[str, bytes, dict]):
        if isinstance(message, dict):
            message = json.dumps(message, cls=JsonEncoderEx)
        if conn[1]:  # send_bytes
            if isinstance(message, str):
                message = message.encode('utf-8')
        elif isinstance(message, bytes):
            message = message.decode('utf-8')
        if conn[1]:
            return await conn[0].send_bytes(message)
        else:
            return await conn[0].send_text(message)

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
