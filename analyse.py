from collections.abc import Callable
from dataclasses import dataclass
from enum import global_str
from parser import Application, Assignment, Expression, Lambda, Value, parse_src

from config import PRETTY_LAMBDAS
from pointer import Ref
from tokens import LiteralInt


@dataclass
class TypableValue:
    name: str
    id: int

    def __str__(self):
        return f"{self.name} :: {self.id}"

    __repr__ = __str__


@dataclass
class TypableLambda:
    param_like: TypableValue
    body: "TypableExpr"

    def __str__(self):
        if PRETTY_LAMBDAS:
            return f"(λ{self.param_like.name} :: {self.param_like.id}.{self.body})"
        else:
            return f"(\\{self.param_like.name} :: {self.param_like.id} -> {self.body})"

    __repr__ = __str__


@dataclass
class TypableApplication:
    fn: "TypableExpr"
    val: "TypableExpr"

    def __str__(self):
        return f"{self.fn}({self.val})"

    __repr__ = __str__


@dataclass
class TypableGlobal:
    name: str
    index: int

    def __str__(self):
        return f"{self.name} || {self.index}"

    __repr__ = __str__


TypableExpr = (
    TypableValue | TypableLambda | TypableApplication | LiteralInt | TypableGlobal
)


@dataclass
class TypableAssignment:
    name: str
    val: TypableExpr

    def __str__(self):
        return f"{self.name} = {self.val}"

    __repr__ = __str__


def find[T](elements: list[T], match: Callable[[T], bool]) -> tuple[T, int] | None:
    for k, el in enumerate(elements):
        if match(el):
            return (el, k)
    return None


def analyse_impl(
    expr: Expression,
    stack: list[tuple[str, int]],
    id_counter: Ref[int],
    globals: dict[str, int],
) -> TypableExpr:
    match expr:
        case Value(name):
            if id := find(stack, lambda el: el[0] == name):
                return TypableValue(name, id[0][1])
            assert name in globals.keys(), f"Global function {name} is not defined"
            return TypableGlobal(name, globals[name])
        case Lambda(var, body):
            param_id = id_counter[:]
            stack.append((var, param_id))
            id_counter *= id_counter[:] + 1
            body = analyse_impl(body, stack, id_counter, globals)
            stack.pop()
            return TypableLambda(TypableValue(var, param_id), body)
        case Application(func, value):
            typable_func = analyse_impl(func, stack, id_counter, globals)
            typable_value = analyse_impl(value, stack, id_counter, globals)
            return TypableApplication(typable_func, typable_value)
        case LiteralInt(v):
            return LiteralInt(v)


def analyse(program: list[Assignment]) -> list[TypableAssignment]:
    globals = {assignment.name: index for index, assignment in enumerate(program)}
    id_counter = Ref(0)
    globals["show"] = id_counter[:]
    id_counter *= id_counter[:] + 1
    globals["add"] = id_counter[:]
    id_counter *= id_counter[:] + 1
    return [
        TypableAssignment(
            assignment.name, analyse_impl(assignment.val, [], id_counter, globals)
        )
        for assignment in program
    ]


def analyse_src(src: str) -> list[TypableAssignment]:
    return analyse(parse_src(src))
