#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Analizador Sintactico
from Compiler.src.SyntacticAnalyzer.Parser import Parser

# Representación Intermedia de Codigo
from Compiler.src.utils.Global import IntermediateRepresentation

# Assembler
from Compiler.src.Assembler.ParserASM import ParserASM

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

