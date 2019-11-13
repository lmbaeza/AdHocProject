#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ply import lex
from ply.lex import TOKEN

from Compiler.src.SemanticAnalyzer.SemanticAnalyzer import incrementCount

class Lexer(object):

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_EQUALS  = r'='
    t_UPDATE  = r':='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_SEMICOLON = r';'

    # Expresiones regulares para palabras reservadas
    t_DOUBLE  = r'(double)'
    t_INT     = r'(int)'
    t_BOOLEAN = r'(boolean)'
    t_STRING  = r'(string)'
    t_PRINT   = r'(print)'
    t_PRINTLN = r'(println)'

    # Expresiones regulares para comparadores
    t_EQUAL    = r'\=\='
    t_NOTEQ    = r'\!\='
    t_LARGE    = r'\>'
    t_LARGE_EQ = r'\>\='
    t_SMALL    = r'\<'
    t_SMALL_EQ = r'\<\='

    t_LCURLY_BRACKET = r'\{'
    t_RCURLY_BRACKET = r'\}'

    # Ignorar Caracteres
    t_ignore = ' \t'


    def __init__(self, *args, **kwargs):

        self.tokens = [
            'ID','INTEGER', 'FLOAT', 'BOOL', 'STRING_CHAIN',
            'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
            'LPAREN','RPAREN', 'SEMICOLON', 'UPDATE',
            'EQUAL', 'NOTEQ', 'LARGE', 'LARGE_EQ', 'SMALL', 'SMALL_EQ',
            'LCURLY_BRACKET', 'RCURLY_BRACKET'
        ]

        self.keywordws = {
            'int': 'INT',
            'double' : 'DOUBLE',
            'boolean': 'BOOLEAN',
            'string':'STRING',
            'print': 'PRINT',
            'println': 'PRINTLN',
            'if': 'IF',
        }

        self.tokens +=  list([v for k, v in self.keywordws.items()])

        self.lexer = lex.lex(module=self, **kwargs)

    @TOKEN(r'[-+]?[0-9]+\.[0-9]+')
    def t_FLOAT(self, t):
        # [-+]?[0-9]+(\.[0-9]+)([eE][-+]?[0-9]+)?
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

    
    @TOKEN(r'(true)|(false)')
    def t_BOOL(self, t):
        
        return t

    # https://stackoverflow.com/questions/12067592/flex-python-ply-regex-for-strings

    @TOKEN(r'("[^"]*")|(\'[^\']*\')')
    def t_STRING_CHAIN(self, t):
        return t


    @TOKEN(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def t_ID(self, t):
        

        if t.value in self.keywordws:
            t.value = t.value.upper();
            t.type = t.value
        return t


    @TOKEN(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)
        incrementCount(len(t.value))


    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    
    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: break
            print(tok)
    

    def getToken(self):
        return self.tokens

