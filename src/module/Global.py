from module.Console import Console


class Global:
    """单例模式，全局变量"""
    _members = {}
    __dict__ = _members

    exit_code = 0  # 退出码
    time_to_exit = False  # 是时候退出了

    debug_mode = False  # 调试模式
    user_config = None  # 用户配置
    console: Console = None  # 控制台对象
    command: str = ''  # 命令

    args_known = ()  # 命令行参数
    args_unknown = ()  # 未知命令

    # def __setattr__(self, key, value):
    #     self._members[key] = value
    #
    # def __getattr__(self, key):
    #     try:
    #         return self._members[key]
    #     except KeyError:
    #         return None
    #
    # def __delattr__(self, key):
    #     del self._members[key]

    def __repr__(self):
        return self._members.__repr__()

    def __getitem__(self, item):
        return self._members[item]

    def __setitem__(self, key, value):
        self._members[key] = value

    def __delitem__(self, key):
        del self._members[key]

    def __iter__(self):
        return iter(self._members)

    def items(self):
        return self._members.items()

    def keys(self):
        return self._members.keys()

    def values(self):
        return self._members.values()

    def clear(self):
        self._members.clear()


Global = Global()

if __name__ == '__main__':
    Global.a = 1
    Global['b'] = 2

    for k, v in Global.items():
        print(k, v)
