class HttpResult:
    """HTTP请求结果类"""
    @staticmethod
    def success(data=None, msg='', code=200) -> dict:
        """200"""
        return {'code': code, 'msg': msg, 'data': data}

    @staticmethod
    def nothing_changed(msg='Nothing changed.') -> dict:
        """304"""
        return {'code': 304, 'msg': msg}

    @staticmethod
    def bad_request(msg='Bad request.') -> dict:
        """400"""
        return {'code': 400, 'msg': msg, 'data': None}

    @staticmethod
    def no_auth(msg='Not authorized.') -> dict:
        """401"""
        return {'code': 401, 'msg': msg, 'data': None}

    @staticmethod
    def forbidden(msg='Forbidden.') -> dict:
        """403"""
        return {'code': 403, 'msg': msg, 'data': None}

    @staticmethod
    def not_found(msg='Not found.') -> dict:
        """404"""
        return {'code': 404, 'msg': msg, 'data': None}

    @staticmethod
    def error(msg='System error.', code=500) -> dict:
        """500"""
        return {'code': code, 'msg': msg, 'data': None}
