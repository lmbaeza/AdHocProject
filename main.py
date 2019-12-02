#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Analizador Sintactico
from Compiler.src.SyntacticAnalyzer.Parser import Parser

# Representación Intermedia de Codigo
from Compiler.src.IntermediateCode.IR import IntermediateRepresentation

# Assembler
from Compiler.src.Assembler.ParserASM import ParserASM
from Compiler.src.Assembler.Code import AssemblyCode

parser = Parser()

# Generación de Codigo Intemedio
with open('example/code.apl', 'r') as file:
    parser.run(file.read())

ir = IntermediateRepresentation()
ir.saveFile()

# Gemeración de codigo Ensamblador
parser = ParserASM()

with open('script.ir', 'r') as file:
    parser.run(file.read())

assembly = AssemblyCode()

assembly.saveFile()