import time

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from module.Global import Global
from module.LoggerEx import LoggerEx, LogLevel


class HttpServer(FastAPI):
    def __init__(self):
        super().__init__(docs_url='/docs', redoc_url='/redoc', title='KenkoGo')
        self.log = LoggerEx('HttpServer')
        if Global.debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug('HttpServer Starting...')
        self.add_event_handler('startup', func=self.server_startup)
        self.add_event_handler('shutdown', func=self.server_shutdown)
        self.add_middleware(BaseHTTPMiddleware, dispatch=self.http_middleware)

    async def server_startup(self):
        self.log.debug('HttpServer Startup.')

    async def server_shutdown(self):
        self.log.debug('HttpServer Shutdown.')

    async def http_middleware(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time  # 请求处理完毕
        response.headers['X-Process-Time'] = str(process_time)
        self.log.debug(f'{request.method:.4s} {process_time:.3f}ms {response.status_code} {request.url.path}')
        return response
