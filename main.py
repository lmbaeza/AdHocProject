#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Compiler.src.SyntacticAnalyzer.Parser import Parser
from Compiler.src.utils.Global import IntermediateRepresentation

parser = Parser()

with open('code.apl', 'r') as file:
    parser.run(file.read())

ir = IntermediateRepresentation()
ir.saveFile()

