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
class LiteralInt:
    value: int

    def __str__(self) -> str:
        return str(self.value)

    __repr__ = __str__


Token = Eq | Arrow | Backslash | LParen | RParen | Identifier | LiteralInt

def tokenise_line(src: str) -> list[Token]:
    ptr = 0
    build = ""
    toks: list[Token] = []

    def flush_cur():
        nonlocal build
        if build == "":
            return
        if (build[0] == "-" and build[1:].isdigit()) or build.isdigit():
            toks.append(LiteralInt(int(build)))
        else:
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
                    assert (
                        False
                    ), f"Error when tokenising '{src}' > from -> without 1 - preceeding, had {cur}"
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
    return [x for x in [tokenise_line(x) for x in src.split("\n")] if len(x) != 0]

