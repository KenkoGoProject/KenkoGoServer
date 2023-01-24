from dataclasses import dataclass
from typing import Sequence


@dataclass
class ConsoleArgument:
    name: str
    flags: Sequence[str]
    action: str
    help_text: str
