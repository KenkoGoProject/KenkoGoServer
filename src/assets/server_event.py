import time
from enum import Enum


class EventType(Enum):
    NEED_SCAN = 'need_scan'


class ServerEvent:
    """服务器事件"""

    @staticmethod
    def gocq_event(event_data):
        return {
            'time': int(time.time()),
            'post_type': 'server_event',
            'server_event_type': 'gocq_event',
            'message': event_data
        }
