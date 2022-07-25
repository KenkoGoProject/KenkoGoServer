from collections import UserDict

import ruamel.yaml as yaml

from module.atomicwrites import atomic_write


class YamlConfig(UserDict):
    def __init__(self, path, auto_load=True, auto_save=True, auto_create=True):
        super().__init__()
        self.path = path
        self.yaml_controller = yaml.YAML()
        self.auto_save = auto_save
        self.auto_create = auto_create
        if auto_load:
            self.load()

    def load(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.data.update(self.yaml_controller.load(f))
        except FileNotFoundError:
            if self.auto_create:
                self.save()
            else:
                raise

    def save(self):
        with atomic_write(self.path, overwrite=True, encoding='utf-8') as f:
            self.yaml_controller.dump(self.data, f)

    # def __getitem__(self, key):
    #     try:
    #         return super(YamlConfig, self).__getitem__(key)
    #     except KeyError:
    #         return None

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.auto_save:
            self.save()
