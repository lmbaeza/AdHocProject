# Variable Global

# VariableGlobal : Singleton

class VariableGlobal:

    class __VariableGlobal:

        def __init__(self):
            self.count = 1
            self.table = {}
            self.variableCounter = 0
            self.labelCounter = 0
            self.comparisonCounter = 0
        
        def __str__(self):
            return repr(self) + self.val
        
        def incrementCount(self, number):
            self.count += number
        
        def incrementVariableCounter(self):
            self.variableCounter += 1
            return self.variableCounter
        
        def incrementLabelCounter(self):
            self.labelCounter += 1
            return self.labelCounter
        
        def incrementComparisonCounter(self):
            self.comparisonCounter += 1
            return self.comparisonCounter
        
        def setTable(self, key, value):
            self.table[key] = value

        def getTable(self, key):
            return self.table.get(key)
  
    instance = None

    def __init__(self):
        if not VariableGlobal.instance:
            VariableGlobal.instance = VariableGlobal.__VariableGlobal()


    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return str(self.instance)
    
    def incrementCount(self, number):
        self.instance.incrementCount(number)
    
    def incrementVariableCounter(self):
        return self.instance.incrementVariableCounter()
    
    def incrementLabelCounter(self):
        return self.instance.incrementLabelCounter()
    
    def incrementComparisonCounter(self):
        return self.instance.incrementComparisonCounter()
    
    def setTable(self, key, value):
        self.instance.setTable(key, value)
    
    def getTable(self, key):
        return self.instance.getTable(key)
    
    def getT(self):
        return self.instance.table
    
    def getCount(self):
        return self.instance.count


def getCode(parser):
    return '~ '+parser.lexer.lexdata.split('\n')[parser.slice[1].lineno-1]

