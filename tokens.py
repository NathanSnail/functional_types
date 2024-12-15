from dataclasses import dataclass

from main import LiteralInt


@dataclass
class Identifier:
    name: str


@dataclass
class Eq:
    pass


@dataclass
class Arrow:
    pass


@dataclass
class LParen:
    pass


@dataclass
class RParen:
    pass


@dataclass
class Backslash:
    pass


@dataclass
class LiteralInt:
    value: int

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


Token = Eq | Arrow | Backslash | LParen | RParen | Identifier | LiteralInt
