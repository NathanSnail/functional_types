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


class Expression:
    pass


@dataclass
class Assignment:
    variable: str
    value: Expression


def parse_statement(toks: list[Token]) -> Expression:
    ptr = 0
    while True:
        pass


def parse_line(toks: list[Token]) -> Assignment:
    match toks[0]:
        case Identifier(var_name):
            name = var_name
        case x:
            raise Exception(f"invalid first token {x} in line {toks}")
    match toks[1]:
        case Eq():
            pass
        case x:
            raise Exception(f"invalid second token {x} in line {toks}")
    return Assignment(name, parse_statement(toks[2:]))


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
    return toks


def tokenise_src(src: str) -> list[list[Token]]:
    return [tokenise_line(x) for x in src.split("\n")]


content = open("./src.func", "r").read()
print(tokenise_src(content))
