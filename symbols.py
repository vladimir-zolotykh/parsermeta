#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
from enum import Enum
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
    return func


class Token:
    @ensure_types
    def __init__(self, sym: Sym, val: float | str):
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
