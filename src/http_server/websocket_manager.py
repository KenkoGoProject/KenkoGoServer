import asyncio
import contextlib
import json
from typing import List, Tuple, Union

from fastapi import WebSocket

from common.logger_ex import LoggerEx, LogLevel
from common.singleton_type import SingletonType
from module.global_dict import Global
from module.json_encoder_ex import JsonEncoderEx


class WebsocketManager(metaclass=SingletonType):
    """WebSocket连接管理器"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} Initializing...')

        self.active_connections: List[Tuple[WebSocket, bool]] = []  # 存活连接

    async def connect(self, websocket: WebSocket, blob: bool = False) -> None:
        """接受新的WebSocket连接

        :param websocket: WebSocket连接
        :param blob: 是否使用blob编码
        """
        await websocket.accept()  # 接受连接
        client = websocket.client
        self.log.info(f'New client connection: {client.host}:{client.port}')
        self.active_connections.append((websocket, blob))

    def disconnect(self, websocket: WebSocket) -> None:
        """断开连接

        :param websocket: WebSocket连接
        """
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

    def broadcast_sync(self, message: Union[str, bytes, dict]):
        try:
            loop = asyncio.get_running_loop()
            loop = loop.create_task
        except RuntimeError:
            loop = asyncio.new_event_loop()
            loop = loop.run_until_complete
        loop(self.broadcast(message))

    def close_all(self):  # 未实现
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        for connection in self.active_connections:
            with contextlib.suppress(ValueError):
                loop.run_until_complete(connection[0].close())
