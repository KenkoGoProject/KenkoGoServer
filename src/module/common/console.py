from rich.console import Console as RichConsole
from rich.pretty import pprint as pretty_print

from module.common.singleton_type import SingletonType


class Console(RichConsole, metaclass=SingletonType):
    def __init__(self):
        super().__init__()

    @staticmethod
    def print_object(_object, **kwargs) -> None:
        pretty_print(_object, expand_all=True, **kwargs)


if __name__ == '__main__':
    console = Console()
