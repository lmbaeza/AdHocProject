#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Compiler.src.SyntacticAnalyzer.Parser import Parser

parser = Parser()

# parser.shell()

with open('code.apl', 'r') as file:
    parser.test(file.read())

