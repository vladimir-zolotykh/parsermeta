#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import types
import inspect
import node as N
from parser import Parser


class Method:
    def __init__(self):
        self.methods = {}

    def register(self, func):
        sig = inspect.signature(func)
        typ = (parm.annotation for _, parm in sig.parameters.items())[1:]
        self.methods[typ] = func

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        typ = (type(a) for a in args)[1:]
        return self.methods[typ](*args, **kwargs)


class MultiDict(dict):
    def __setitem__(self, key, func):
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, func)
        else:
            self.setdefault(key, Method()).register(func)


class MultiMeta(type):
    @classmethod
    def __prepare__(name, bases, ns):
        return MultiDict()


class Visitor(metaclass=MultiMeta):
    def visit(self, n: N.Num) -> float:
        return n.val

    def visit(self, n: N.Plus) -> float:  # noqa: F811
        return self.visit(n.left) + self.visit(n.right)

    def visit(self, n: N.Minus) -> float:  # noqa: F811
        return self.visit(n.left) - self.visit(n.right)

    def visit(self, n: N.Mul) -> float:  # noqa: F811
        return self.visit(n.left) * self.visit(n.right)

    def visit(self, n: N.Div) -> float:  # noqa: F811
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n = Parser().parse(sexpr)
    print(Visitor().visit(n))
