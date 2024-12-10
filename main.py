from dataclasses import dataclass
from typing import Dict

from tokens import Arrow, Backslash, Eq, Identifier, LParen, RParen, Token


@dataclass
class Value:
    name: str


@dataclass
class Lambda:
    param_name: str
    body: "Expression"


@dataclass
class Application:
    fn: "Expression"
    val: "Expression"


Expression = Value | Lambda | Application


def parse_value(toks: list[Token]) -> tuple[Expression, int]:
    ptr = 0
    match toks[ptr]:
        case LParen():
            ptr += 1
            (expr, skip) = parse_statement(toks[ptr:])
            ptr += 1
            assert type(toks[ptr + skip]) is RParen, "Paren not closed"
            return (expr, ptr)
        case Backslash():
            ptr += 1
            param_name = toks[ptr]
            assert (
                type(param_name) is Identifier
            ), "Lambda param is not an identifier"
            print(param_name)
            ptr += 1
            assert type(toks[ptr]) is Arrow, "Lambda missing arrow"
            ptr += 1
            (val, skip) = parse_statement(toks[ptr:])
            ptr += skip
            return (Lambda(param_name.name, val), ptr)
        case Identifier(name):
            return (Value(name), 1)
    assert False, "invalid token for value"


def parse_statement(toks: list[Token]) -> tuple[Expression, int]:
    ptr = 0
    vars: list[str] = []
    while True:
        cur = toks[ptr]
        match cur:
        ptr += 1


def parse_line(toks: list[Token]) -> Assignment:
    id = toks[0]
    assert (
        type(id) is Identifier
    ), f"Declaration name {id} is not an identifier for {toks}"
    assert (
        type(toks[1]) is Eq
    ), f"Declaration does not have a equals, has {toks[1]} for {toks}"
    return Assignment(id.name, parse_statement(toks[2:]))


def tokenise_line(src: str) -> list[Token]:
    ptr = 0
    build = ""
    toks: list[Token] = []

    def flush_cur():
        nonlocal build
        if build == "":
            return
        toks.append(Identifier(build))
        build = ""

    srclen = len(src)
    while ptr < srclen:
        cur = src[ptr]
        match cur:
            case "=":
                flush_cur()
                toks.append(Eq())
            case "\\":
                flush_cur()
                toks.append(Backslash())
            case "-":
                flush_cur()
                cur = "-"
            case ">":
                if cur != ">":
                    raise Exception(
                        f"Error when tokenising '{src}' > from -> without 1 - preceeding, had {cur}"
                    )
                toks.append(Arrow())
            case "(":
                flush_cur()
                toks.append(LParen())
            case ")":
                flush_cur()
                toks.append(RParen())
            case " ":
                flush_cur()
            case x:
                build = build + x
        ptr += 1
    flush_cur()
    return toks


def tokenise_src(src: str) -> list[list[Token]]:
    return [tokenise_line(x) for x in src.split("\n")]


content = open("./src.func", "r").read()
toks = tokenise_src(content)
print(toks)
parse_line(toks[0])
