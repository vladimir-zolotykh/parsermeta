#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import symbols as S


class Node:
    @S.ensure_types
    def __init__(self, val: float | S.Sym):
        self.val = val


class Num(Node):
    @S.ensure_types
    def __init__(self, val: float):
        super().__init__(val)

    def __repr__(self):
        return f"{type(self).__name__}({self.val!r})"


class BinOp(Node):
    @S.ensure_types
    def __init__(self, left: Node, right: Node):
        super().__init__(self._op)
        self.left, self.right = left, right

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"


class Plus(BinOp):
    _op = S.Sym.PLUS


class Minus(BinOp):
    _op = S.Sym.MINUS


class Mul(BinOp):
    _op = S.Sym.MUL


class Div(BinOp):
    _op = S.Sym.DIV
