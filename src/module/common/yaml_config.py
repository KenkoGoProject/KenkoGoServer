from collections import UserDict

import ruamel.yaml as yaml

from module.common.atomicwrites import atomic_write


class YamlConfig(UserDict):
    """yaml 文件读写操作"""

    def __init__(self, path: str, auto_load=True, auto_create=True):
        """yaml文件操作类

        :param path: yaml文件路径
        :param auto_load: 自动加载文件
        :param auto_create: 自动创建文件
        """
        super().__init__()
        self.path = path
        self.yaml_controller = yaml.YAML()
        self.data = {}
        self.auto_create = auto_create
        if auto_load:
            self.load()

    def load(self) -> None:
        """重新加载文件"""
        try:
            with open(self.path, encoding='utf-8') as f:
                self.data.update(self.yaml_controller.load(f))
        except FileNotFoundError:
            if self.auto_create:
                self.save()
            else:
                raise

    def save(self) -> None:
        """保存文件"""
        with atomic_write(self.path, overwrite=True, encoding='utf-8') as f:
            self.yaml_controller.dump(self.data, f)

    def cover(self, new_data: dict) -> None:
        """设置为新的数据

        :param new_data: 新的数据
        """
        self.data = new_data
