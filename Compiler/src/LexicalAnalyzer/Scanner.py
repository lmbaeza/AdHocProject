#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ply import lex
from ply.lex import TOKEN

from Compiler.src.utils.Global import VariableGlobal

varGlobal = VariableGlobal()

class Lexer(object):

    # Expresiones regulares para tokens simples
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_EQUALS  = r'='
    t_UPDATE  = r':='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_SEMICOLON = r';'
    t_LCURLY_BRACKET = r'\{'
    t_RCURLY_BRACKET = r'\}'

    # Expresiones regulares para palabras reservadas
    t_DOUBLE  = r'(double)'
    t_INT     = r'(int)'
    t_BOOLEAN = r'(boolean)'
    t_STRING  = r'(string)'
    t_PRINT   = r'(print)'
    t_PRINTLN = r'(println)'
    t_FN      = r'(fn)'
    t_MAIN    = r'(main)'
    t_VOID    = r'(void)'
    t_WHILE   = r'(while)'

    # Expresiones regulares para comparadores
    t_EQUAL    = r'\=\='
    t_NOTEQ    = r'\!\='
    t_LARGE    = r'\>'
    t_LARGE_EQ = r'\>\='
    t_SMALL    = r'\<'
    t_SMALL_EQ = r'\<\='

    

    # Ignorar Caracteres
    t_ignore = ' \t'


    def __init__(self, *args, **kwargs):

        # Tokens
        self.tokens = [
            'ID','INTEGER', 'FLOAT', 'BOOL', 'STRING_CHAIN',
            'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
            'LPAREN','RPAREN', 'SEMICOLON', 'UPDATE',
            'EQUAL', 'NOTEQ', 'LARGE', 'LARGE_EQ', 'SMALL', 'SMALL_EQ',
            'LCURLY_BRACKET', 'RCURLY_BRACKET'
        ]

         # Reserved Keywords
        self.keywordws = {
            'int': 'INT',
            'double' : 'DOUBLE',
            'boolean': 'BOOLEAN',
            'string':'STRING',
            'void': 'VOID',
            'print': 'PRINT',
            'println': 'PRINTLN',
            'if': 'IF',
            'else': 'ELSE',
            'fn': 'FN',
            'main': 'MAIN',
            'while': 'WHILE'
        }
    
        self.tokens +=  list([v for k, v in self.keywordws.items()])

        self.lexer = lex.lex(module=self, **kwargs)

        

    # Regla de expresión regular para flotantes, que el asigna el valor del flotante al token
    @TOKEN(r'[-+]?[0-9]+\.[0-9]+')
    def t_FLOAT(self, t):
        # [-+]?[0-9]+(\.[0-9]+)([eE][-+]?[0-9]+)?
        t.value = float(t.value)
        return t

    # Regla de expresión regular para enteros, que el asigna el valor del entero al token, así como un manejo de error para entradas muy grandes
    @TOKEN(r'\d+')
    def t_INTEGER(self, t):
        
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    # Regla de expresión regular para booleanos.
    @TOKEN(r'(true)|(false)')
    def t_BOOL(self, t):
        return t

    # Reglas de expresión regular para strings.
    # https://stackoverflow.com/questions/12067592/flex-python-ply-regex-for-strings

    @TOKEN(r'("[^"]*")|(\'[^\']*\')')
    def t_STRING_CHAIN(self, t):
        return t

    # Regla de epresión regular para identificadores, que le asigna el string del identificador al token en mayúsculas.
    @TOKEN(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def t_ID(self, t):
        if t.value in self.keywordws:
            t.value = t.value.upper();
            t.type = t.value
        return t

    # Regla de expresión regular para el salto de linea
    @TOKEN(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)
        varGlobal.incrementCount(len(t.value))

    # Mensaje de error para caracteres desconocidos
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    
    def test(self,data):
        out = ''
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: break
            out += str(tok) + '\n'
        return out
    

    def getToken(self):
        return self.tokens

