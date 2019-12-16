from tkinter import ttk
from tkinter import *

from Compiler.src.LexicalAnalyzer.Scanner import Lexer
from Compiler.src.SyntacticAnalyzer.Parser import Parser
from Compiler.src.IntermediateCode.IR import IntermediateRepresentation
from Compiler.src.Assembler.ParserASM import ParserASM
from Compiler.src.Assembler.Code import AssemblyCode
from Compiler.src.utils.GlobalASM import VariableGlobalASM
from Compiler.src.utils.Global import VariableGlobal

sample1 = None

with open('example/sample-1.apl', 'r') as file:
    sample1 = file.read()

sample2 = None

with open('example/sample-2.apl', 'r') as file:
    sample2 = file.read()

sample3 = None

with open('example/sample-3.apl', 'r') as file:
    sample3 = file.read()

class Windows:
    def __init__(self, windows):
        self.win = windows
        self.win.title("Fases de un Compilador")
        frame = LabelFrame(self.win,text='Compilador AdHoc')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        self.btn1 = ttk.Button(frame, text="Generar Tokens", command=self.onClickBtn1)
        self.btn1.grid(row=3, columnspan=2, sticky=W+E)
        

        self.btn2 = ttk.Button(frame, text="Generar Codigo Intermedio", command=self.onClickBtn2)
        self.btn2.grid(row=4, columnspan=2, sticky=W+E)
        self.btn2["state"] = "disabled"

        self.btn3 = ttk.Button(frame, text="Generar Codigo Assembler", command=self.onClickBtn3)
        self.btn3.grid(row=5, columnspan=2, sticky=W+E)
        self.btn3["state"] = "disabled"
        
        self.reset = ttk.Button(frame, text="Reset", command=self.onClickReset)
        self.reset.grid(row=4, column=2, columnspan=2, sticky=W+E)

        variable = StringVar(frame)
        variable.set("Sample 1") # default value
        options = ["Sample 1", "Sample 2", "Sample 3"]
        self.select = OptionMenu(frame, variable, *(options),command=self.onselect)
        self.select.grid(row=3, columnspan=2, column=2)

        self.codeTxt = Text(frame, height=20, width=50)
        self.codeTxt.grid(row=6,column=1)
        self.codeTxt.insert(END, sample1)

        self.resultTxt = Text(frame, height=20, width=50)
        self.resultTxt.grid(row=6, column=2, sticky=W+E)
        self.resultTxt.insert(END, '')
        self.resultTxt['state'] = 'disabled'
    
    def onselect(self, event):
        self.codeTxt.delete(1.0, END)
        if str(event) == 'Sample 1':
            self.codeTxt.insert(INSERT, sample1)
        elif str(event) == 'Sample 2':
            self.codeTxt.insert(INSERT, sample2)
        elif str(event) == 'Sample 3':
            self.codeTxt.insert(INSERT, sample3)
        self.btn1['state'] = 'normal'
        self.btn2['state'] = 'disabled'
        self.btn3['state'] = 'disabled'
        self.clearResult()

    # BTN: Analizador Lexico
    # Tokens
    def onClickBtn1(self):
        if str(self.btn2['state']) == 'disabled':
            self.btn2['state'] = 'normal'
            self.btn1['state'] = 'disabled'
            self.btn3['state'] = 'disabled'
        lexer = Lexer()
        out = lexer.test(self.codeTxt.get(1.0, END))
        self.resultTxt['state'] = 'normal'
        self.resultTxt.delete(1.0, END)
        self.resultTxt.insert(INSERT, str(out))
        self.resultTxt['state'] = 'disabled'
        
    # BTN: Analizador Sintactico y Semantico
    # Representación Intermedia de Codigo
    def onClickBtn2(self):
        if str(self.btn3['state']) == 'disabled':
            self.btn3['state'] = 'normal'
            self.btn2['state'] = 'disabled'
            self.btn1['state'] = 'disabled'
        parser = Parser()
        parser.run(self.codeTxt.get(1.0, END))
        ir = IntermediateRepresentation()
        ir.saveFile()
        self.resultTxt['state'] = 'normal'
        self.resultTxt.delete(1.0, END)
        self.resultTxt.insert(INSERT, str(ir.getCode()))
        self.resultTxt['state'] = 'disabled'
        ir.clear()
        varGlobal = VariableGlobal()
        varGlobal.clear()

    # BTN: Fase de Ensamblaje
    # Lenguaje Ensamblador
    def onClickBtn3(self):
        if str(self.btn1['state']) == 'disabled':
            self.btn1['state'] = 'disabled'
            self.btn2['state'] = 'disabled'
            self.btn3['state'] = 'disabled'
        
        parser = ParserASM()
        self.resultTxt['state'] = 'normal'
        parser.run(self.resultTxt.get(1.0, END))
        asm = AssemblyCode()
        asm.saveFile()
        self.resultTxt.delete(1.0, END)
        self.resultTxt.insert(INSERT, str(asm.getCode()))
        self.resultTxt['state'] = 'disabled'

        asm.clear()
        asmGlobal = VariableGlobalASM()
        asmGlobal.clear()
    
    def onClickReset(self):
        self.codeTxt.delete(1.0, END)
        if str(self.select['text']) == 'Sample 1':
            self.codeTxt.insert(INSERT, sample1)
        elif str(self.select['text']) == 'Sample 2':
            self.codeTxt.insert(INSERT, sample2)
        elif str(self.select['text']) == 'Sample 3':
            self.codeTxt.insert(INSERT, sample3)

        self.btn1['state'] = 'normal'
        self.btn2['state'] = 'disabled'
        self.btn3['state'] = 'disabled'
        self.clearResult()
    
    def clearResult(self):
        self.resultTxt['state'] = 'normal'
        self.resultTxt.delete(1.0, END)
        self.resultTxt['state'] = 'disabled'
        ir = IntermediateRepresentation()
        ir.clear()
        varGlobal = VariableGlobal()
        varGlobal.clear()
        asm = AssemblyCode()
        asm.clear()
        asmGlobal = VariableGlobalASM()
        asmGlobal.clear()
        