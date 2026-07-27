#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import symbols as S
import node as N

PLUS = S.Sym.PLUS
MINUS = S.Sym.MINUS
MUL = S.Sym.MUL
DIV = S.Sym.DIV
LPAREN = S.Sym.LPAREN
RPAREN = S.Sym.RPAREN


def new_binop(op: S.Sym, left: N.Node, right: N.Node) -> N.BinOp:
    return {PLUS: N.Plus, MINUS: N.Minus, MUL: N.Mul, DIV: N.Div}[op.sym](left, right)


class Parser:
    def __init__(self):
        self.token: S.Token | None = S.Token | None
        self.tokens: Iterator[S.Token] | None = None

    def _advance(self) -> S.Token | None:
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.token = None
        return self.token

    def _expect(self, expected: S.Sym) -> None:
        if (tok := self.token) != expected:
            raise SyntaxError(f"Got {tok}, expected {expected}")
        self._consume()

    def _consume(self) -> None:
        self.token = next(self.tokens)

    def expr(self) -> N.Node:
        res: N.Node = self.term()
        while (op := self.token) and op in (PLUS, MINUS):
            self._consume()
            right: N.Node = self.term()
            res = new_binop(op, res, right)
        return res

    def term(self) -> N.Node:
        res: N.Node = self.factor()
        while (op := self.token) and op in (MUL, DIV):
            self._consume()
            right: N.Node = self.factor()
            res = new_binop(op, res, right)
        return res

    def factor(self) -> N.Node:
        tok: S.Token = self.token
        if tok == LPAREN:
            self._consume()
            res = self.expr()
            self._expect(RPAREN)
        else:
            res = N.Num(float(tok.val))
            self._advance()
        return res

    def parse(self, sexpr: str):
        self.tokens = S.iter_tokens(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    print(Parser().parse(sexpr))
