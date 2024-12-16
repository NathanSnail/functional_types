from dataclasses import dataclass

from tokens import (Arrow, Backslash, Eq, Identifier, LiteralInt, LParen,
                    RParen, Token, tokenise_src)

from config import PRETTY_LAMBDAS


@dataclass
class Value:
    name: str

    def __str__(self):
        return self.name

    __repr__ = __str__


@dataclass
class Lambda:
    param_name: str
    body: "Expression"

    def __str__(self):
        if PRETTY_LAMBDAS:
            return f"(λ{self.param_name}.{self.body})"
        else:
            return f"(\\{self.param_name} -> {self.body})"

    __repr__ = __str__


@dataclass
class Application:
    fn: "Expression"
    val: "Expression"

    def __str__(self):
        return f"{self.fn}({self.val})"

    __repr__ = __str__


Expression = Value | Lambda | Application | LiteralInt


@dataclass
class Assignment:
    name: str
    val: Expression

    def __str__(self):
        return f"{self.name} = {self.val}"

    __repr__ = __str__


def parse_value(toks: list[Token]) -> tuple[Expression, int]:
    ptr = 0
    match toks[ptr]:
        case LParen():
            ptr += 1
            (expr, skip) = parse_statement(toks[ptr:])
            ptr += skip
            assert (
                type(toks[ptr]) is RParen
            ), f"Paren not closed, got {toks[ptr]} and had {toks}"
            ptr += 1
            return (expr, ptr)
        case Backslash():
            ptr += 1
            param_name = toks[ptr]
            assert (
                type(param_name) is Identifier
            ), f"Lambda param is not an identifier, got {param_name} and had {toks}"
            ptr += 1
            assert (
                type(toks[ptr]) is Arrow
            ), f"Lambda missing arrow, got {toks[ptr]} and had {toks}"
            ptr += 1
            (val, skip) = parse_statement(toks[ptr:])
            ptr += skip
            return (Lambda(param_name.name, val), ptr)
        case LiteralInt(value):
            return (LiteralInt(value), 1)
        case Identifier(name):
            return (Value(name), 1)
    assert False, f"invalid token {toks[ptr]} for value, had {toks}"


def parse_statement(toks: list[Token]) -> tuple[Expression, int]:
    (built, ptr) = parse_value(toks)
    while True:
        if len(toks) == ptr or type(toks[ptr]) is RParen:
            return (built, ptr)
        (expr, skip) = parse_value(toks[ptr:])
        built = Application(built, expr)
        ptr += skip


def parse_line(toks: list[Token]) -> Assignment:
    id = toks[0]
    assert (
        type(id) is Identifier
    ), f"Declaration name {id} is not an identifier for {toks}"
    assert (
        type(toks[1]) is Eq
    ), f"Declaration does not have a equals, has {toks[1]} for {toks}"
    (expr, skip) = parse_statement(toks[2:])
    if len(toks[2:]) != skip:
        assert (
            False
        ), f"Not all tokens consumed for line {toks}, had {toks[2+skip:]} remaining"
    return Assignment(id.name, expr)


def parse_src(src: str) -> list[Assignment]:
    return [parse_line(x) for x in tokenise_src(src)]
