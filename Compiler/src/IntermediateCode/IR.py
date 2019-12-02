
# Representación de Codigo Intermedio

# IntermediateRepresentation : Singleton

class IntermediateRepresentation:
    class _IR:
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
        if not IntermediateRepresentation.instance:
            IntermediateRepresentation.instance = IntermediateRepresentation._IR()

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
    
    def saveFile(self, filename='script.ir'):
        with open(filename, 'w') as file:
            file.write(self.instance.getCode())
            print('Se generó la representación intermedia de codigo correctamente\n')

