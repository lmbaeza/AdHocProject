#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RootException:

    def __init__(self, message, code, line,  filename='<stdin>'):
        self.message = message
        self.line = line
        self.filename = filename
        self.code = code
        self.execute()
        exit(-1)

    def execute(self):
        error = 'Traceback (most recent call last):\n'
        error += '   File "{0}", line {1}, in <module>\n'.format(self.filename, self.line)
        error += '     {0}\n'.format(self.code)
        error += '{0}: {1}\n'.format(self.__class__.__name__, self.message)

        print(error)


class UndeclaredVariable(RootException):
    pass


class IncompatibleTypesException(RootException):
    pass


class IntegerTypeException(RootException):
    pass


class FloatTypeException(RootException):
    pass


class BooleanTypeException(RootException):
    pass


class StringTypeException(RootException):
    pass


class BadOperandException(RootException):
    pass


class TypeErrorException(RootException):
    pass


class NameException(RootException):
    pass

class SyntaxErrorException(RootException):
    pass

class VariableAlreadyDeclared(RootException):
    pass
