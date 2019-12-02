#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ply import lex
from ply.lex import TOKEN


class LexerASM(object):
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_EQUALS  = r'='

    t_EQUAL   = r'\=\=' 
    t_NOT_EQUAL   = r'\!\=' 

    t_ignore = ' \t'

    def __init__(self, *args, **kwargs):
        self.tokens = [
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
            'ID', 'TMP', 'FLOAT', 'INTEGER', 'LABEL', 'EQUAL',
            'NOT_EQUAL'
        ]

        self.keywordws = {
            'IFNOT': 'IFNOT',
            'GOTO': 'GOTO'
        }
    
        self.tokens +=  list([v for k, v in self.keywordws.items()])

        self.lexer = lex.lex(module=self, **kwargs)
    
    @TOKEN(r'[-+]?[0-9]+\.[0-9]+')
    def t_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @TOKEN(r'\d+')
    def t_INTEGER(self, t):
        
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t
    
    @TOKEN(r'\$[a-zA-Z_][a-zA-Z0-9_]*')
    def t_TMP(self, t):
        return t

    @TOKEN(r'\.[a-zA-Z_][a-zA-Z0-9_]*\:')
    def t_LABEL(self, t):
        return t
    
    @TOKEN(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def t_ID(self, t):
        if t.value in self.keywordws:
            t.value = t.value.upper();
            t.type = t.value
        return t
    
    @TOKEN(r'\n')
    def t_newline(self, t):
        pass

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def getToken(self):
        return self.tokens