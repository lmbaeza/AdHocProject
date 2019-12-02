class VariableGlobalASM:
    
    class __VariableGlobalASM:

        def __init__(self):
            self.addressRAM = 0
            self.table = {}
            self.tmp = {}
        
        def __str__(self):
            return repr(self) + self.val
        
        def incrementAddressRAM(self):
            self.addressRAM += 1
        
        def setTable(self, key, value):
            self.table[key] = value

        def getTable(self, key):
            return self.table.get(key)
        
        def setTMP(self, key, value):
            self.tmp[key] = value

        def getTMP(self, key):
            return self.tmp.get(key)
  
    instance = None

    def __init__(self):
        if not VariableGlobalASM.instance:
            VariableGlobalASM.instance = VariableGlobalASM.__VariableGlobalASM()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return str(self.instance)
    
    def incrementAddressRAM(self):
        self.instance.incrementAddressRAM()
    
    def setTable(self, key, value):
        self.instance.setTable(key, value)
    
    def getTable(self, key):
        return self.instance.getTable(key)
    
    def setTMP(self, key, value):
        self.instance.setTMP(key, value)
    
    def getTMP(self, key):
        return self.instance.getTMP(key)
    
    def getTable_(self):
        return self.instance.table
    
    def getTMP_(self):
        return self.instance.tmp
    
    def getAddressRAM(self):
        return self.instance.addressRAM


class Registers(object):

    def __init__(self, R1, R2, R3, R4):
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.R4 = R4