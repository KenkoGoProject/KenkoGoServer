import hashlib
import hmac
import random
import socket

import requests


class Utils:
    """自定义工具类"""

    @staticmethod
    def is_port_in_use(_port: int, _host='127.0.0.1'):
        """检查端口是否被占用"""
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((_host, _port))
            return True
        except socket.error:
            return False
        finally:
            if s:
                s.close()

    @classmethod
    def get_random_free_port(cls):
        """获取一个随机空闲端口"""
        result = random.randint(10000, 65535)
        while cls.is_port_in_use(result):
            result = random.randint(10000, 65535)
        return result

    @staticmethod
    def get_self_ip():
        """
        获取自身ip
        https://www.zhihu.com/question/49036683/answer/1243217025
        """
        s = None
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        finally:
            if s:
                s.close()

    @staticmethod
    def get_public_ip(method: int = 0):
        """获取公网ip"""
        if method == 0:
            return requests.get('https://api.ipify.org').text
        elif method == 1:
            return requests.get('https://api.ip.sb/ip').text
        elif method == 2:
            return requests.get('http://myexternalip.com/raw').text
        elif method == 3:
            return requests.get('http://ip.42.pl/raw').text
        elif method == 4:
            return requests.get('http://myip.ipip.net/').text  # 非纯ip
        elif method == 5:
            return requests.get('http://ipecho.net/plain').text
        elif method == 6:
            return requests.get('http://hfsservice.rejetto.com/ip.php').text

    @staticmethod
    def hash_mac(key: str, content: bytes, alg=hashlib.sha1):
        """hash mac"""
        hmac_code = hmac.new(key.encode(), content, alg)
        return hmac_code.hexdigest()
