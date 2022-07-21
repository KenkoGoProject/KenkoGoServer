class HttpResult:
    """HTTP请求结果类"""
    @staticmethod
    def success(data=None, msg='', code=200):
        return {'code': code, 'msg': msg, 'data': data}

    @staticmethod
    def no_auth(msg='身份未认证'):
        return {'code': 401, 'msg': msg, 'data': None}

    @staticmethod
    def error(status_code=404, msg=''):
        return {'code': status_code, 'msg': msg, 'data': None}
