import json
from typing import Any


class JsonEncoderEx(json.JSONEncoder):
    """自定义JSONEncoder，用于解决JSON序列化时无法序列化某些类型的问题"""

    def default(self, _object) -> Any:
        return super().default(_object)
