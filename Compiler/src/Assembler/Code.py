class AssemblyCode:
    class _AC:
        def __init__(self):
            self.code = ''
        
        def __str__(self):
            return repr(self)
        
        def setCode(self, codestr):
            self.code += '\n' + str(codestr)
        
        def getCode(self):
            return self.code

    instance = None

    def __init__(self):
        if not AssemblyCode.instance:
            AssemblyCode.instance = AssemblyCode._AC()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return str(self.instance)
    
    def setCode(self, codestr, debug=False):
        if debug:
            print(codestr)
        
        self.instance.setCode(codestr)
        
    def getCode(self):
        return self.instance.getCode()
    
    def saveFile(self, filename='script.asm'):
        with open(filename, 'w') as file:
            file.write(self.instance.getCode())
            print('Se generó la representación el codigo ensamblador correctamente\n')
