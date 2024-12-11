from dataclasses import dataclass

from tokens import Arrow, Backslash, Eq, Identifier, LParen, RParen, Token


@dataclass
class Value:
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


@dataclass
class Lambda:
    param_name: str
    body: "Expression"

    def __str__(self):
        return f"\{self.param_name} -> {self.body}"

    def __repr__(self):
        # improper but idc
        return str(self)


@dataclass
class Application:
    fn: "Expression"
    val: "Expression"

    def __str__(self):
        return f"{self.fn}({self.val})"

    def __repr__(self):
        return str(self)


Expression = Value | Lambda | Application


@dataclass
class Assignment:
    name: str
    val: Expression

    def __str__(self):
        return f"{self.name} = {self.val}"

    def __repr__(self):
        return str(self)


def parse_value(toks: list[Token]) -> tuple[Expression, int]:
    ptr = 0
    match toks[ptr]:
        case LParen():
            ptr += 1
            (expr, skip) = parse_statement(toks[ptr:])
            ptr += skip
            assert type(toks[ptr]) is RParen, "Paren not closed"
            ptr += 1
            return (expr, ptr)
        case Backslash():
            ptr += 1
            param_name = toks[ptr]
            assert type(param_name) is Identifier, "Lambda param is not an identifier"
            ptr += 1
            assert type(toks[ptr]) is Arrow, "Lambda missing arrow"
            ptr += 1
            (val, skip) = parse_statement(toks[ptr:])
            ptr += skip
            return (Lambda(param_name.name, val), ptr)
        case Identifier(name):
            return (Value(name), 1)
    assert False, f"invalid token {toks[ptr]} for value"


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
        assert False, f"Not all tokens consumed for line {toks}"
    return Assignment(id.name, expr)


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
    return [x for x in [tokenise_line(x) for x in src.split("\n")] if len(x) != 0]


content = open("./src.func", "r").read()
toks = tokenise_src(content)
for line in toks:
    # print(line)
    print(parse_line(line))
