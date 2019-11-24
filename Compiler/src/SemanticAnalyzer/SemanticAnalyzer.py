#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Compiler.src.SyntacticAnalyzer import Global
from Compiler.src.SyntacticAnalyzer.Global import VariableGlobal
from Compiler.src.Exceptions.Exceptions import *


varGlobal = VariableGlobal()

# def incrementCount(number):
#     Global.count += number

# def incrementVariableCounter():
#     Global.variableCounter += 1
#     return Global.variableCounter

# def incrementLabelCounter():
#     Global.labelCounter += 1
#     return Global.labelCounter

# def incrementComparisonCounter():
#     Global.comparisonCounter += 1
#     return Global.comparisonCounter

# def set(key, value):
#     Global.table[key] = value

# def get(key):
#     return Global.table.get(key)


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

    @staticmethod
    def check(typeName):
        typeName = str(typeName)
        if typeName == "<class 'int'>":
            return 'INT'
        elif typeName == "<class 'float'>":
            return 'BOOLEAN'
        elif typeName == "<class 'str'>":
            return 'STRING'
        elif typeName == "<class 'bool'>":
            return 'BOOLEAN'

# Clase padre para todas las Expresiones
class Expression(object):
    def evaluate(self):
        # Aca se implementa cada tipo de expresion.
        raise NotImplementedError

# Expresión para los Numeros Flotantes
class Float(Expression):

    def __init__(self, value):
        self.value = float(value)
    
    def evaluate(self):
        return self.value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
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

# Expresión para los Numeros Enteros
class Integer(Expression):
    
    def __init__(self, value):
        self.value = int(value)
    
    def evaluate(self):
        return self.value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
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

# Expresiones Booleanas
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
            return '1'
        elif not self.value:
            return '0'
    
    def __str__(self):
        return self.evaluate()
    
    def __repr__(self):
        return self.evaluate()
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)
    
    def __ne__(self, other):
        return Boolean(self.value != other.value)


# Expresiones de String
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


# Lista de Expresiones
class StatementList(Expression):
    
    def __init__(self, value, next):
        self.value = value
        self.next = next

    def evaluate(self):
        if self.value is not None:
            self.value.evaluate()
        return self.next

# Expresion de la sentencia IF
# if (comparison) {
#     <expresion>
#     ...........
#     <expresion>
# }
class StatementIf(Expression):

    def __init__(self, typeName, comparison, next_):
        self.type = typeName
        self.comparison = comparison
        self.next = next_

    def evaluate(self):
        number = varGlobal.incrementLabelCounter()
        comp = self.comparison.evaluate()
        print('IFNOT {comp} GOTO :ENDIF'.format(comp=comp)+str(number)+':')
        nextTmp = self.next

        while nextTmp is not None:
            tmp = nextTmp.evaluate()
            nextTmp = tmp
        print(':ENDIF'+str(number)+':')

# Expresion de la sentencia IF-ELSE
# if (comparison) {
#     <expresion>
#     ...........
#     <expresion>
# } else {
#     <expresion>
#     ...........
#     <expresion>
# }
class StatementIfElse(Expression):
    
    def __init__(self, typeName, comparison, nextif, nextelse):
        self.type = typeName
        self.comparison = comparison
        self.nextIf = nextif
        self.nextElse = nextelse

    def evaluate(self):
        number = varGlobal.incrementLabelCounter()
        comp = self.comparison.evaluate()
        print('IFNOT {comp} GOTO :ELSE_'.format(comp=comp)+str(number)+':')
        nextTmp = self.nextIf

        while nextTmp is not None:
            tmp = nextTmp.evaluate()
            nextTmp = tmp
        
        numberElse = varGlobal.incrementLabelCounter()
        print('GOTO :ENDIF_{id}:'.format(id=numberElse))

        print(':ELSE_'+str(number)+':')
        
        nextTmp = self.nextElse

        while nextTmp is not None:
            tmp = nextTmp.evaluate()
            nextTmp = tmp
        
        print(':ENDIF_{id}:'.format(id=numberElse))


# Expresion de Asignación
# int x = 0;
# double x = 0.0;
# boolean x = true;
class StatementAssign(Expression):
    
    def __init__(self, typeName, dataType, p,varName, value):
        self.typeName = typeName
        self.dataType = dataType
        self.p = p
        self.varName = varName
        self.value = value
        self.table = varGlobal.getT()
        
        

    def evaluate(self):

        if self.table.get(self.varName) is not None:
            message = "variable '{0}' is already defined".format(self.varName)
            code = self.p.lexer.lexdata
            line = Global.count
            VariableAlreadyDeclared(message, code, line)

        val = self.value.evaluate()
        code = self.p.lexer.lexdata
        line = Global.count
        
        if isinstance(self.value, ExpressionID):
        
            if self.dataType == 'BOOLEAN':
                if not self.table.get(val):
                    IncompatibleTypesException("Incompatible Types", code, line)
            elif (self.table.get(val) is None) or \
                    self.dataType != Type.check(type(self.table.get(val).evaluate())):
                IncompatibleTypesException("Incompatible Types", code, line)
        
        varGlobal.setTable(self.varName, self.value)

        self.table = varGlobal.getT()

        t = type(val)


        if str(t)=="<class 'int'>":
            val = Integer(val)
        elif str(t)=="<class 'float'>":
            val = Float(val)
        elif str(t)=="<class 'bool'>":
            val = Boolean(val)
        # Revisar para string
        
        if isinstance(val, str):
            print(self.varName + ' = ' + str(val))
            return val
        elif self.dataType==Type.INT and isinstance(val, Integer):
            print(self.varName + ' = ' + str(val))
            return val
        elif self.dataType==Type.DOUBLE and isinstance(val, Float):
            print(self.varName + ' = ' + str(val))
            return val
        elif self.dataType==Type.BOOLEAN and isinstance(val, Boolean):
            print(self.varName + ' = ' + str(val))
            return val
        elif self.dataType==Type.STRING and isinstance(val, String):
            print(self.varName + ' = ' + str(val))
            return val
        else:
            IncompatibleTypesException("Incompatible Types", code, line)



# class StatementExpr(Expression):
#     def __init__(self, p, value):
#         self.p = p
#         self.value = value

#     def evaluate(self):
        
#         if isinstance(self.value, Expression):
#             print(self.value.evaluate())


# Expresion de actualización
# x := 0;
# x := 0.0;
# x := true;
class StatementUpdate(Expression):
    
    def __init__(self, typeName, p, varName, value):
        self.typeName = typeName
        self.p = p
        self.varName = varName
        self.value = value
        self.table = varGlobal.getT()
        self.oldType = None

    def evaluate(self):
        self.oldType = self.table.get(self.varName)

        if self.oldType is None:
            message = "variable '{0}' has not been declared".format(self.varName)
            code = self.p.lexer.lexdata
            line = Global.count
            UndeclaredVariable(message, code, line)
        
        val = self.value.evaluate()
        code = self.p.lexer.lexdata
        line = Global.count
        
        varGlobal.setTable(self.varName, self.value)

        self.table = varGlobal.getT()

        t = type(val)

        if str(t)=="<class 'int'>":
            val = Integer(val)
        elif str(t)=="<class 'float'>":
            val = Float(val)
        elif str(t)=="<class 'bool'>":
            val = Boolean(val)
        # Revisar para string
        
        if isinstance(self.oldType, Integer) and isinstance(val, Integer):
            print(self.varName + ' = ' + str(val))
            return val
        elif isinstance(self.oldType, Float) and isinstance(val, Float):
            print(self.varName + ' = ' + str(val))
            return val
        elif isinstance(self.oldType, Boolean) and isinstance(val, Boolean):
            print(self.varName + ' = ' + str(val))
            return val
        elif isinstance(self.oldType, String) and isinstance(val, String):
            print(self.varName + ' = ' + str(val))
            return val
        else:
            if isinstance(self.value, ExpressionID):
                if str(type(self.table.get(val))) == str(type(self.oldType)):
                    print(self.varName + ' = ' + str(val))
                    return
            elif isinstance(self.value, ExpressionBinop):
                print(self.varName + ' = ' + str(val))
                return
            elif isinstance(self.value, ExpressionGroup):
                print(self.varName + ' = ' + str(val))
                return

            IncompatibleTypesException("Incompatible Types", code, line)


# Expresion de Operacion Binaria
# a + b
# a - b
# a * b
# a / b
class ExpressionBinop(Expression):
    
    def __init__(self,typeName,  p, varName, left, right, operator):
        self.typeName = typeName
        self.p = p
        self.varName = varName + str(varGlobal.incrementVariableCounter())
        self.left = left
        self.right = right
        self.operator = operator

    def evaluate(self):
        if isinstance(self.left, ExpressionGroup):
            self.left = self.left.evaluate()
        
        if isinstance(self.right, ExpressionGroup):
            self.right = self.right.evaluate()

        if isinstance(self.left, ExpressionBinop):
            self.left = self.left.evaluate()
        
        if isinstance(self.right, ExpressionBinop):
            self.right = self.right.evaluate()
        
        if isinstance(self.left, ExpressionID):
            self.left = self.left.evaluate()
        
        if isinstance(self.right, ExpressionID):
            self.right = self.right.evaluate()

        print('{x} = {y} {op} {z}'.format(
            x=self.varName,
            y=self.left,
            op=self.operator,
            z=self.right
        ))
        
        return self.varName


# Expresion de Comparación para Operadores Binarios
# a > b, a >= b
# a < b, a <= b
class ComparisonBinop(Expression):
    
    def __init__(self, typeName, p, varName, left, right, operator):
        self.typeName = typeName
        self.p = p
        self.varName = varName + str(varGlobal.incrementComparisonCounter())
        self.left = left
        self.right = right
        self.operator = operator
        self.table = varGlobal.getT()

    def evaluate(self):

        if isinstance(self.left, ExpressionGroup):
            self.left = self.left.evaluate()
        
        if isinstance(self.right, ExpressionGroup):
            self.right = self.right.evaluate()

        if isinstance(self.left, ExpressionBinop):
            self.left = self.left.evaluate()
        
        if isinstance(self.right, ExpressionBinop):
            self.right = self.right.evaluate()
        
        if isinstance(self.left, ExpressionID):
            self.left = self.left.evaluate()
        
        if isinstance(self.right, ExpressionID):
            self.right = self.right.evaluate()
        
        print('{x} = {y} {op} {z}'.format(
            x=self.varName,
            y=self.left,
            op=self.operator,
            z=self.right
        ))

        return self.varName

# Expresion para Negación
# -a
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

# Expresion con parentesis
# (a + b)
class ExpressionGroup(Expression):
    
    def __init__(self, p, value):
        self.p = p
        self.value = value

    def evaluate(self):
        return self.value.evaluate()


# Expresion para obtener ID
class ExpressionID(Expression):

    def __init__(self, p, name):
        self.p = p
        self.name = name
        self.value = varGlobal.getTable(name)

    def evaluate(self):
        # if self.value is  None:
        #     message = " name '{0}' is not defined".format(self.name)
        #     code = self.p.lexer.lexdata
        #     line = Global.count
        #     NameException(message, code, line)
        
        return self.name


# class Print(Expression):
#     def __init__(self, p, value):
#         self.p = p
#         self.value = value
#
#     def evaluate(self):
#
#         print(self.value.evaluate(), end='')
#
#
# class Println(Expression):
#   
#     def __init__(self, p, value):
#         self.p = p
#         self.value = value
#
#     def evaluate(self):
#
#         print(self.value.evaluate())


# Expresion para Errores de Sintaxis
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

