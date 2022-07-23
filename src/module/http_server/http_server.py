import time

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from module.controller.gocq_bin_controller import GocqBinController
from module.controller.instance_controller import InstanceController
from module.global_dict import Global
from module.http_result import HttpResult
from module.logger_ex import LoggerEx, LogLevel


class HttpServer(FastAPI):
    def __init__(self):
        super().__init__(docs_url='/docs', redoc_url=None, title='KenkoGo')
        self.log = LoggerEx('HttpServer')
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug('HttpServer Initializing...')

        self.add_event_handler('startup', func=self.server_startup)
        self.add_event_handler('shutdown', func=self.server_shutdown)
        self.add_middleware(BaseHTTPMiddleware, dispatch=self.http_middleware)

        self.router.add_api_route('/', self.route_root, methods=['GET', 'POST'])
        self.router.include_router(GocqBinController())
        self.router.include_router(InstanceController())

    async def server_startup(self):
        self.log.debug('HttpServer Startup.')

    async def server_shutdown(self):
        self.log.debug('HttpServer Shutdown.')

    async def http_middleware(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)  # 请求处理
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        self.log.debug(f'{request.method:.4s} {process_time:.3f}s {response.status_code} '
                       f'{request.url.path} {request.query_params}')
        return response

    @classmethod
    async def route_root(cls):
        return HttpResult.success('This is KenkoGo!')
