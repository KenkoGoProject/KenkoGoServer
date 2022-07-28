import time

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from assets.http_result import HttpResult
from module.controller.client_controller import ClientController
from module.controller.gocq_bin_controller import GocqBinController
from module.controller.information_controller import InformationController
from module.controller.instance_controller import InstanceController
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel


class HttpServer(FastAPI):
    # TODO: 此处应使用单例模式

    def __init__(self):
        """初始化"""
        super().__init__(docs_url='/docs', redoc_url=None, title=Global().app_name)  # 关闭 redoc
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug(f'{self.__class__.__name__} initializing...')

        self.add_event_handler('startup', func=self.server_startup)
        self.add_event_handler('shutdown', func=self.server_shutdown)
        self.add_middleware(BaseHTTPMiddleware, dispatch=self.http_middleware)
        self.add_exception_handler(HTTPException, handler=self.exception_handler_ex)

        self.router.add_api_route('/', self.route_root, methods=['GET', 'POST'])
        self.router.include_router(GocqBinController())
        self.router.include_router(InstanceController())
        self.router.include_router(InformationController())
        self.router.include_router(ClientController())
        self.router.add_api_route('*', self.route_404,
                                  methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])

    @staticmethod
    async def exception_handler_ex(_: Request, exc: HTTPException) -> JSONResponse:
        """异常处理"""
        headers = getattr(exc, 'headers', None)
        if exc.status_code == 404:
            content = HttpResult.not_found(exc.detail)
        else:
            content = HttpResult.error(exc.detail)
        return JSONResponse(content=content, status_code=exc.status_code, headers=headers)

    async def server_startup(self) -> None:
        """事件 服务启动"""
        self.log.debug('HttpServer startup.')
        self.log.debug(f'Try from http://{Global().host_with_port}')
        self.log.info(f'{Global().app_name} started at '
                      f'http://{Global().user_config.host}:{Global().user_config.port} .')
        self.log.info('Try in https://kenkogo.akagiyui.com')

    async def server_shutdown(self) -> None:
        """事件 服务关闭"""
        self.log.warning('HttpServer shutdown.')

    async def http_middleware(self, request: Request, call_next) -> JSONResponse:
        """请求中间件"""
        self.log.debug(f'{request.method:.4s} {request.url.path} {request.query_params}')
        start_time = time.time()
        response = await call_next(request)  # 请求处理
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        self.log.debug(f'{response.status_code}  Process Time: {process_time:.3f}s')
        return response

    @staticmethod
    async def route_root() -> dict:
        """根路由"""
        return HttpResult.success(f'This is {Global().app_name}!')

    @staticmethod
    async def route_404() -> dict:
        """404路由"""
        return HttpResult.not_found('Not Found')
