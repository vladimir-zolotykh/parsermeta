#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import get_type_hints, get_origin, get_args, Any
from functools import wraps
from enum import Enum
import inspect
import re

Sym = Enum(
    "Sym",
    {
        k: f"(?P<{k}>{v})"
        for k, v in {
            "NAME": r"[A-Za-z_][\w]*",
            "NUM": r"\d+",
            "LPAREN": r"\(",
            "RPAREN": r"\)",
            "PLUS": r"\+",
            "MINUS": r"-",
            "MUL": r"\*",
            "DIV": r"/",
            "WS": r"\s+",
        }.items()
    },
)


def ensure_types(func):
    sig = inspect.signature(func)
    hints = get_type_hints(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, parm in bound.arguments.items():
            if name in hints:
                assert isinstance(name, get_args(hints[name]))
        res = func(*args, **kwargs)
        return res

    return wrapper


class Token:
    @ensure_types
    def __init__(self, sym: Sym, val: float | str = ""):
        self.sym = sym
        self.val = val

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        elif isinstance(other, Sym):
            return self.sym == other
        else:
            return NotImplemented

    def __repr__(self):
        args = ", ".join(f"{str(x)!r}" for x in self.__dict__.values())
        return f"{type(self).__name__}({args})"


def iter_tokens(sexpr: str):
    master_pat = "|".join(s.value for s in Sym)
    for match in re.finditer(master_pat, sexpr):
        if (g := match.lastgroup) != Sym.WS.name:
            yield Token(Sym[g], match.group(0))


if __name__ == "__main__":
    for t in iter_tokens("2 + (3 * 4) + 5"):
        print(t)
