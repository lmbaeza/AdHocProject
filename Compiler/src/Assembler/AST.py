from .Code import AssemblyCode
from Compiler.src.utils.GlobalASM import VariableGlobalASM

assembly = AssemblyCode()

globalASM = VariableGlobalASM()


class Expression(object):
    def evaluate(self):
        raise NotImplementedError

R1 = 'ax'
R2 = 'dx'
R3 = 'bx'
R4 = 'cx'

# Lista de Sentencias
# <statement>
# ...
# ...
# <statement>
class StatementList(Expression):
    def __init__(self, typeName, value, _next):
        self.typeName = typeName
        self.value = value
        self.next = _next

    def evaluate(self):
        if self.value is not None:
            data = self.value.evaluate()
            if data:
                assembly.setCode(data)
        
        return self.next

# identificador = x operador y
class StatementAssignID(Expression):
    def __init__(self, typeName, ID, op, value):
        self.typeName = typeName
        self.id = ID
        self.op = op
        self.value = value

    def evaluate(self):

        if not globalASM.getTable(self.id):
            globalASM.incrementAddressRAM()
            globalASM.setTable(self.id, globalASM.getAddressRAM())

        if isinstance(self.id, Expression):
            self.id = self.id.evaluate()
        if isinstance(self.op, Expression):
            self.op = self.op.evaluate()
        
        if isinstance(self.value, ExpressionInteger):
            self.value = self.value.evaluate()

            return '\tCARGAR PTR[{addr}], {value}'.format(
                addr=globalASM.getTable(self.id), value=self.value
            )
        elif isinstance(self.value, ExpressionID):
            out = '\tCARGAR {r1}, PTR[{addr}]'.format(
                r1=R1,
                addr=globalASM.getTable(self.value.evaluate())
            )
            out += '\n\tCARGAR PTR[{addr}], {r1}'.format(
                addr=globalASM.getTable(self.id), r1=R1
            )

            return out
        elif isinstance(self.value, Expression):
            self.value = self.value.evaluate()


        return '\tCARGAR PTR[{addr}], {r1}'.format(
            addr=globalASM.getTable(self.id), r1=R3
        )

# $tmp = x operator y
class StatementAssignTMP(Expression):
    def __init__(self, typeName, tmp, op, value):
        self.typeName = typeName
        self.tmp = tmp
        self.op = op
        self.value = value

    def evaluate(self):

        out = '\tCOPIAR {}, {}'.format(R3, R1)
        
        # tmp[self.tmp] = {'r':R3, "op": self.value.evaluate()}
        globalASM.setTMP(self.tmp, {'r':R3, "op": self.value.evaluate()})
        return out

# x operator y
class ExpressionBinop(Expression):
    def __init__(self, typeName, left, op, right):
        self.typeName = typeName
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):

        if isinstance(self.left, ExpressionInteger) or\
            isinstance(self.left, ExpressionFloat):
            self.left = self.left.evaluate()
        elif isinstance(self.left, ExpressionID):
            number = globalASM.getTMP(self.left.evaluate())
            number = number.get('r')
            self.left = 'PTR['+number+']'
        elif isinstance(self.left, ExpressionTMP):
            number = globalASM.getTMP(self.left.evaluate())
            number = number.get('r')
            self.left = number
        

        if isinstance(self.op, Expression):
            self.op = self.op.evaluate()


        if isinstance(self.right, ExpressionInteger) or\
            isinstance(self.right, ExpressionFloat):
            self.right = self.right.evaluate()
        elif isinstance(self.right, ExpressionID):
            number = globalASM.getTMP(self.right.evaluate())
            number = number.get('r')
            self.right = 'PTR['+number+']'
        elif isinstance(self.right, ExpressionTMP):
            number = globalASM.getTMP(self.right.evaluate())
            number = number.get('r')
            self.right = number
        
        assembly.setCode('\tCOPIAR {r1}, {value}'.format(
            r1=R1,
            value=str(self.left)
        ))
        assembly.setCode('\tCOPIAR {r2}, {value}'.format(
            r2=R2,
            value=str(self.right)
        ))
        # return str(self.left) + ' ' + str(self.op) + ' ' + str(self.right)

        if self.op == '+':
            return assembly.setCode('\tSUMA {r1}, {r2}'.format(r1=R1, r2=R2))
        elif self.op == '-':
            return assembly.setCode('\tRESTA {r1}, {r2}'.format(r1=R1, r2=R2))
        elif self.op == '*':
            return assembly.setCode('\tMULT {r1}, {r2}'.format(r1=R1, r2=R2))
        elif self.op == '/':
            return assembly.setCode('\tDIV {r1}, {r2}'.format(r1=R1, r2=R2))

# x == y
# x != y
class ExpressionComparison(Expression):
    def __init__(self, typeName, left, op, right):
        self.typeName = typeName
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):

        
        if isinstance(self.left, ExpressionID):
            self.left = self.left.evaluate()
            
            assembly.setCode('\tCOPIAR {r1}, PTR[{addr}]'.format(
                r1=R1,
                addr=globalASM.getTable(self.left)
            ))
            
        if isinstance(self.right, ExpressionID):
            self.right = self.right.evaluate()
            assembly.setCode('\tCOPIAR {r2}, PTR[{addr}]'.format(
                r2=R2,
                addr=globalASM.getTable(self.right)
            ))
        elif isinstance(self.right, ExpressionInteger):
            self.right = self.right.evaluate()
            assembly.setCode('\tCOPIAR {r2}, {num}'.format(
                r2=R2,
                num=self.right
            ))
        
        return str(self.op)

# -x
class ExpressionUminus(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(-self.value)

# number
class ExpressionInteger(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(self.value)

# Float
class ExpressionFloat(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(self.value)

# x = y
class ExpressionID(Expression):
    def __init__(self, typeName, ID):
        self.typeName = typeName
        self.id = ID

    def evaluate(self):
        return str(self.id)

# x = $var1
class ExpressionTMP(Expression):
    def __init__(self, typeName, tmp):
        self.typeName = typeName
        self.tmp = tmp

    def evaluate(self):
        return str(self.tmp)

# IFNOT comparison GOTO .label:
class ExpressionIFNOT(Expression):
    def __init__(self, typeName, comparison, label):
        self.typeName = typeName
        self.comparison = comparison
        self.label = label

    def evaluate(self):
        
        out = '\tCOMPARAR {r1}, {r2}'.format(
            r1=R1,
            r2=R2
        )

        data = globalASM.getTMP(self.comparison)

        if data.get('op'):
            if data.get('op') == '==':
                out += '\n\tSALTO_SI_UNO '+self.label
            elif data.get('op') == '==':
                out += '\n\SALTO_SI_CERO '+self.label
        
        return out
        
# GOTO .label:
class ExpressionGOTO(Expression):
    def __init__(self, typeName, value, label):
        self.typeName = typeName
        self.value = value
        self.label = label

    def evaluate(self):
        return '\tSALTAR' + ' ' + self.label

# .label:
class ExpressionLABEL(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(self.value)

