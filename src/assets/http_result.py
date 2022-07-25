class HttpResult:
    """HTTP请求结果类"""
    @staticmethod
    def success(data=None, msg='', code=200):
        return {'code': code, 'msg': msg, 'data': data}

    @staticmethod
    def error(msg='System error.', code=500):
        return {'code': code, 'msg': msg, 'data': None}

    @staticmethod
    def no_auth(msg='Not authorized.'):
        return {'code': 401, 'msg': msg, 'data': None}

    @staticmethod
    def not_found(msg='Not found.'):
        return {'code': 404, 'msg': msg, 'data': None}
