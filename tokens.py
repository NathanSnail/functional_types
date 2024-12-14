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


@dataclass
class IntToken:
    value: int
    pass


Token = Eq | Arrow | Backslash | LParen | RParen | Identifier | IntToken
