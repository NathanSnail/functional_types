from dataclasses import dataclass


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


Token = Eq | Arrow | Backslash | LParen | RParen | Identifier
