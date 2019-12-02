
class Expression(object):
    def evaluate(self):
        raise NotImplementedError

countRAM = 0

table = {}
tmp = {}

R1 = 'ax'
R2 = 'dx'
R3 = 'bx'
R4 = 'cx'

class StatementList(Expression):
    def __init__(self, typeName, value, _next):
        self.typeName = typeName
        self.value = value
        self.next = _next

    def evaluate(self):
        if self.value is not None:
            data = self.value.evaluate()
            if data:
                print(data)
        
        return self.next

class StatementAssignID(Expression):
    def __init__(self, typeName, ID, op, value):
        self.typeName = typeName
        self.id = ID
        self.op = op
        self.value = value

    def evaluate(self):
        global countRAM
        countRAM += 1
        table[self.id] = countRAM

        # print(self.value)

        if isinstance(self.id, Expression):
            self.id = self.id.evaluate()
        if isinstance(self.op, Expression):
            self.op = self.op.evaluate()
        
        if isinstance(self.value, ExpressionInteger):
            self.value = self.value.evaluate()

            return '\tCARGAR PTR[{addr}], {value}'.format(
                addr=table.get(self.id), value=self.value
            )
        elif isinstance(self.value, Expression):
            self.value = self.value.evaluate()


        return '\tCARGAR PTR[{addr}], {r1}'.format(
            addr=table.get(self.id), r1=R3
        )


class StatementAssignTMP(Expression):
    def __init__(self, typeName, tmp, op, value):
        self.typeName = typeName
        self.tmp = tmp
        self.op = op
        self.value = value

    def evaluate(self):
        global countRAM
        #countRAM += 1

        out = '\tCOPIAR {}, {}'.format(R3, R1)
        
        tmp[self.tmp] = {'r':R3, "op": self.value.evaluate()}
        return out
        # if isinstance(self.tmp, Expression):
        #     self.tmp = self.tmp.evaluate()
        # if isinstance(self.op, Expression):
        #     self.op = self.op.evaluate()
        # if isinstance(self.value, Expression):
        #     self.value = self.value.evaluate()

        

class StatementExpr(Expression):
    def __init__(self, typeName, expr):
        self.typeName = typeName
        self.expr = expr

    def evaluate(self):
        return '\tExpr'

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
            number = tmp.get(self.left.evaluate())
            number = number.get('r')
            self.left = 'PTR['+number+']'
        elif isinstance(self.left, ExpressionTMP):
            number = tmp.get(self.left.evaluate())
            number = number.get('r')
            self.left = number
        

        if isinstance(self.op, Expression):
            self.op = self.op.evaluate()


        if isinstance(self.right, ExpressionInteger) or\
            isinstance(self.right, ExpressionFloat):
            self.right = self.right.evaluate()
        elif isinstance(self.right, ExpressionID):
            number = tmp.get(self.right.evaluate())
            number = number.get('r')
            self.right = 'PTR['+number+']'
        elif isinstance(self.right, ExpressionTMP):
            number = tmp.get(self.right.evaluate())
            number = number.get('r')
            self.right = number
        
        print('\tCOPIAR {r1}, {value}'.format(
            r1=R1,
            value=str(self.left)
        ))
        print('\tCOPIAR {r2}, {value}'.format(
            r2=R2,
            value=str(self.right)
        ))
        # return str(self.left) + ' ' + str(self.op) + ' ' + str(self.right)

        if self.op == '+':
            return print('\tSUMA {r1}, {r2}'.format(r1=R1, r2=R2))
        elif self.op == '-':
            return print('\tRESTA {r1}, {r2}'.format(r1=R1, r2=R2))
        elif self.op == '*':
            return print('\tMULT {r1}, {r2}'.format(r1=R1, r2=R2))
        elif self.op == '/':
            return print('\tDIV {r1}, {r2}'.format(r1=R1, r2=R2))

class ExpressionComparison(Expression):
    def __init__(self, typeName, left, op, right):
        self.typeName = typeName
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):

        
        if isinstance(self.left, ExpressionID):
            self.left = self.left.evaluate()
            
            print('\tCOPIAR {r1}, PTR[{addr}]'.format(
                r1=R1,
                addr=table.get(self.left)
            ))
            
        # if isinstance(self.op, Expression):
        #     self.op = self.op.evaluate()
        

        if isinstance(self.right, ExpressionID):
            self.right = self.right.evaluate()
            print('\tCOPIAR {r2}, PTR[{addr}]'.format(
                r2=R2,
                addr=table.get(self.right)
            ))
        elif isinstance(self.right, ExpressionInteger):
            self.right = self.right.evaluate()
            print('\tCOPIAR {r2}, {num}'.format(
                r2=R2,
                num=self.right
            ))
        
        return str(self.op)

class ExpressionUminus(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(-self.value)

class ExpressionInteger(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(self.value)

class ExpressionFloat(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(self.value)

class ExpressionID(Expression):
    def __init__(self, typeName, ID):
        self.typeName = typeName
        self.id = ID

    def evaluate(self):
        return str(self.id)

class ExpressionTMP(Expression):
    def __init__(self, typeName, tmp):
        self.typeName = typeName
        self.tmp = tmp

    def evaluate(self):
        return str(self.tmp)

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

        data = tmp.get(self.comparison)

        if data.get('op'):
            if data.get('op') == '==':
                out += '\n\tSALTO_SI_UNO '+self.label
            elif data.get('op') == '==':
                out += '\n\SALTO_SI_CERO '+self.label
        
        return out
        

class ExpressionGOTO(Expression):
    def __init__(self, typeName, value, label):
        self.typeName = typeName
        self.value = value
        self.label = label

    def evaluate(self):
        return '\t'+str(self.value) + ' ' + self.label

class ExpressionLABEL(Expression):
    def __init__(self, typeName, value):
        self.typeName = typeName
        self.value = value

    def evaluate(self):
        return str(self.value)