#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Compiler.src.SyntacticAnalyzer import Global
from Compiler.src.Exceptions.Exceptions import *

def incrementCount(number):
    Global.count += number


class Type:
    # Variables Estaticas
    TYPE_INT = "<class 'int'>"
    TYPE_FLOAT = "<class 'float'>"
    TYPE_STR = "<class 'str'>"
    TYPE_BOOL = "<class 'bool'>"
    
    INT = 'INT'
    DOUBLE = 'DOUBLE'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'


class Expression(object):
    def evaluate(self):
        # Aca se implementa cada tipo de expresion.
        raise NotImplementedError


class Float(Expression):

    def __init__(self, value):
        self.value = float(value)
    
    def evaluate(self):
        return self.value
    
    def __add__(self, other):
        return Float(self.value + other.value)

    def __sub__(self, other):
        return Float(self.value - other.value)

    def __mul__(self, other):
        return Float(self.value * other.value)

    def __truediv__(self, other):
        return Float(self.value / other.value)
    
    def __gt__(self, other):
        return Boolean(self.value > other.value)
    
    def __ge__(self, other):
        return Boolean(self.value >= other.value)
    
    def __lt__(self, other):
        return Boolean(self.value < other.value)
    
    def __le__(self, other):
        return Boolean(self.value <= other.value)
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)
    
    def __ne__(self, other):
        return Boolean(self.value != other.value)

    def __neg__(self):
        return Float(-self.value)


class Integer(Expression):
    
    def __init__(self, value):
        self.value = int(value)
    
    def evaluate(self):
        return self.value
    
    def __add__(self, other):
        return Integer(self.value + other.value)

    def __sub__(self, other):
        return Integer(self.value - other.value)

    def __mul__(self, other):
        return Integer(self.value * other.value)

    def __truediv__(self, other):
        return Integer(self.value / other.value)
    
    def __gt__(self, other):
        return Boolean(self.value > other.value)
    
    def __ge__(self, other):
        return Boolean(self.value >= other.value)
    
    def __lt__(self, other):
        return Boolean(self.value < other.value)
    
    def __le__(self, other):
        return Boolean(self.value <= other.value)
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)
    
    def __ne__(self, other):
        return Boolean(self.value != other.value)
    
    def __neg__(self):
        return Integer(-self.value)


class Boolean(Expression):
    
    def __init__(self, value):
        self.value = None
        if value == 'true' or value == True:
            self.value = bool(True)
        elif value == 'false'or value == False:
            self.value = bool(False)
        else:
            # BooleanTypeException('Error: Boolean Type: ')
            pass
            
    
    def evaluate(self):
        if self.value:
            return 'true'
        elif not self.value:
            return 'false'
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)
    
    def __ne__(self, other):
        return Boolean(self.value != other.value)


class String(Expression):
    
    def __init__(self, value):
        self.value = str(value)
    
    def evaluate(self):
        aux = self.value
        aux = aux[1 : len(aux)-1]
        return aux
    
    def __add__(self, other):
        return Integer(self.value + other.value)

    def __sub__(self, other):
        return Integer(self.value - other.value)

    def __mul__(self, other):
        return Integer(self.value * other.value)

    def __truediv__(self, other):
        return Integer(self.value / other.value)
    
    def __gt__(self, other):
        return Boolean(self.value > other.value)
    
    def __ge__(self, other):
        return Boolean(self.value >= other.value)
    
    def __lt__(self, other):
        return Boolean(self.value < other.value)
    
    def __le__(self, other):
        return Boolean(self.value <= other.value)
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)
    
    def __ne__(self, other):
        return Boolean(self.value != other.value)


class StatementAssign(Expression):
    
    def __init__(self, p, variableType, value, tableValue, varName):
        self.p = p
        self.variableType = variableType
        self.value = value
        self.tableValue = tableValue
        self.varName = varName

    def evaluate(self):
        if self.tableValue is not None:
            message = "variable '{0}' variable x is already defined".format(self.varName)
            code = self.p.lexer.lexdata
            line = Global.count
            VariableAlreadyDeclared(message, code, line)

        val = self.value

        code = self.p.lexer.lexdata
        line = Global.count

        if self.variableType==Type.INT and isinstance(self.value, Integer):
            return val
        elif self.variableType==Type.DOUBLE and isinstance(self.value, Float):
            return val
        elif self.variableType==Type.BOOLEAN and isinstance(self.value, Boolean):
            return val
        elif self.variableType==Type.STRING and isinstance(self.value, String):
            return val
        else:
            IncompatibleTypesException("Incompatible Types", code, line)



class StatementExpr(Expression):
    def __init__(self, p, value):
        self.p = p
        self.value = value

    def evaluate(self):
        
        if isinstance(self.value, Expression):
            print(self.value.evaluate())



class StatementUpdate(Expression):
    
    def __init__(self, p,varName, oldType, value):
        self.p = p
        self.varName = varName
        self.value = value
        self.oldType = None

        if oldType is not None:
            self.oldType = oldType
        else:
            message = "variable '{0}' has not been declared".format(self.varName)
            code = self.p.lexer.lexdata
            line = Global.count
            UndeclaredVariable(message, code, line)


    def evaluate(self):
        val = self.value

        code = self.p.lexer.lexdata
        line = Global.count

        if isinstance(self.oldType, Integer) and isinstance(self.value, Integer):
            return val
        elif isinstance(self.oldType, Float) and isinstance(self.value, Float):
            return val
        elif isinstance(self.oldType, Boolean) and isinstance(self.value, Boolean):
            return val
        elif isinstance(self.oldType, String) and isinstance(self.value, String):
            return val
        else:
            IncompatibleTypesException("Incompatible Types", code, line)


class ExpressionBinop(Expression):
    
    def __init__(self, p, left, right, operator):
        self.p = p
        self.left = left
        self.right = right
        self.operator = operator

    def evaluate(self):

        if isinstance(self.left, Integer) and isinstance(self.right, Integer):
            if self.operator == '+':
                return self.left + self.right
            elif self.operator == '-':
                return self.left - self.right
            elif self.operator == '*':
                return self.left * self.right
            elif self.operator == '/':
                return self.left / self.right
            else:
                message = "unsupported operand type(s) for '{0}'".format(self.operator)
                code = self.p.lexer.lexdata
                line = Global.count
                TypeErrorException(message, code, line)

        elif isinstance(self.left, Float) and isinstance(self.right, Float):
            if self.operator == '+':
                return self.left + self.right
            elif self.operator == '-':
                return self.left - self.right
            elif self.operator == '*':
                return self.left * self.right
            elif self.operator == '/':
                return self.left / self.right
            else:
                message = "unsupported operand type(s) for '{0}'".format(self.operator)
                code = self.p.lexer.lexdata
                line = Global.count
                TypeErrorException(message, code, line)

        else:
            message = "bad operand types for binary operator '{0}'".format(self.operator)
            code = self.p.lexer.lexdata
            line = Global.count
            BadOperandException(message, code, line)


class ComparisonBinop(Expression):
    
    def __init__(self, p, left, right, operator):
        self.p = p
        self.left = left
        self.right = right
        self.operator = operator

    def evaluate(self):

        if type(self.left) == type(self.right) and (isinstance(self.left, Integer) or\
            isinstance(self.left, Float) or isinstance(self.left, String)):
            if self.operator == '==':
                return self.left == self.right
            elif self.operator == '!=':
                return self.left != self.right
            elif self.operator == '>':
                return self.left > self.right
            elif self.operator == '>=':
                return self.left >= self.right
            elif self.operator == '<':
                return self.left < self.right
            elif self.operator == '<=':
                return self.left <= self.right
            else:
                message = "unsupported operand type(s) for '{0}'".format(self.operator)
                code = self.p.lexer.lexdata
                line = Global.count
                TypeErrorException(message, code, line)

        elif type(self.left) == type(self.right) and isinstance(self.left, Boolean):
            if self.operator == '==':
                return self.left == self.right
            elif self.operator == '!=':
                return self.left != self.right
            else:
                message = "unsupported operand type(s) for '{0}'".format(self.operator)
                code = self.p.lexer.lexdata
                line = Global.count
                TypeErrorException(message, code, line)

        else:
            message = "bad operand types for binary operator '{0}'".format(self.operator)
            code = self.p.lexer.lexdata
            line = Global.count
            BadOperandException(message, code, line)


class ExpressionUminus(Expression):
    
    def __init__(self, p, value):
        self.p = p
        self.value = value

    def evaluate(self):
        if isinstance(self.value, Integer) or isinstance(self.value, Float):
            return -self.value;
        else:
            message = "bad operand types for operator '-'"
            code = self.p.lexer.lexdata
            line = Global.count
            BadOperandException(message, code, line)


class ExpressionGroup(Expression):
    
    def __init__(self, p, value):
        self.p = p
        self.value = value

    def evaluate(self):
        return self.value


class ExpressionID(Expression):

    def __init__(self, p, name, value):
        self.p = p
        self.name = name
        self.value = None

        if value is not None:
            self.value = value
        else:
            message = " name '{0}' is not defined".format(self.name)
            code = self.p.lexer.lexdata
            line = Global.count
            NameException(message, code, line)

    def evaluate(self):
        return self.value


class Print(Expression):
    
    def __init__(self, p, value):
        self.p = p
        self.value = value

    def evaluate(self):

        print(self.value.evaluate(), end='')


class Println(Expression):
    
    def __init__(self, p, value):
        self.p = p
        self.value = value

    def evaluate(self):

        print(self.value.evaluate())


class ErrorNotMatch(Expression):

    def __init__(self, p):
        self.p = p

    def evaluate(self):
        
        if self.p is not None:
            message = "Invalid Syntax at '{0}'".format(self.p.value)
            code = self.p.lexer.lexdata
            line = Global.count
            SyntaxErrorException(message, code, line)
        else:
            message = "Invalid Syntax"
            code = ''
            line = Global.count
            SyntaxErrorException(message, code, line)

