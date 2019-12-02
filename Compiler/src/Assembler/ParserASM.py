#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ply import yacc

from Compiler.src.Assembler.LexASM import LexerASM
from Compiler.src.Assembler.AST import *


class ParserASM(object):



    def __init__(self):
        self.tokens = LexerASM().getToken()

        # Se define el nivel de prioridad para la asociación a la hora de reducir y/o desplazar las expresiones
        self.precedence = (
            ('left', 'PLUS', 'MINUS'),
            ('left', 'TIMES', 'DIVIDE'),
            ('right', 'UMINUS'),
        )

        self.lexer = LexerASM()
        self.parser = yacc.yacc(module=self)
    
    def p_run(self, p):
        r'run : statements-list'

        next = p[1]

        while next is not None:
            tmp = next.evaluate()
            next = tmp

    def p_statement_list(self, p):
        r'''statements-list : statement statements-list'''
        p[0] = StatementList('Statement List', p[1], p[2])
        

    
    def p_statement_list_empty(self, p):
        r'''statements-list : '''

    
    def p_statement_assign_id(self, p):
        r'statement : ID EQUALS expression'
        p[0] = StatementAssignID('ASSING_ID', p[1], p[2], p[3])

    def p_statement_assign_tmp(self, p):
        r'statement : TMP EQUALS expression'
        p[0] = StatementAssignTMP('ASSING_TMP', p[1], p[2], p[3])
        

    def p_statement_expr(self, p):
        r'statement : expression'
        p[0] = p[1]
    
    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
        
        if p[2] == '+':
            p[0] = ExpressionBinop('BINOP', p[1], p[2], p[3])
        elif p[2] == '-':
            p[0] = ExpressionBinop('BINOP', p[1], p[2], p[3])
        elif p[2] == '*':
            p[0] = ExpressionBinop('BINOP', p[1], p[2], p[3])
        elif p[2] == '/':
            p[0] = ExpressionBinop('BINOP', p[1], p[2], p[3])
    
    def p_expression_comparison(self, p):
        r'expression : expression EQUAL expression'
        p[0] = ExpressionComparison('COMPARISON', p[1], p[2], p[3])

    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        p[0] = ExpressionUminus('UMINUS', p[2])
    

    def p_expression_integer(self, p):
        "expression : INTEGER"
        p[0] = ExpressionInteger('INT', p[1])


    def p_expression_float(self, p):
        "expression : FLOAT"
        p[0] = ExpressionFloat('FLOAT', p[1])


    def p_expression_id(self, p):
        "expression : ID"
        p[0] = ExpressionID('ID', p[1])
        # p[0] = p[1]
        # try:
        #     p[0] = names[p[1]]
        # except LookupError:
        #     print("Undefined name '%s'" % p[1])
        #     p[0] = 0

    def p_expression_tmp(self, p):
        "expression : TMP"
        p[0] = ExpressionTMP('TMP', p[1])

    def p_expression_ifnot(self, p):
        r'''expression : IFNOT TMP GOTO LABEL
                       | IFNOT ID GOTO LABEL'''
        
        p[0] = ExpressionIFNOT('IFNOT', p[2], p[4])
    
    def p_expression_goto(self, p):
        r'expression : GOTO LABEL'
        p[0] = ExpressionGOTO('GOTO', p[1], p[2])

    def p_expression_label(self, p):
        r'expression : LABEL'
        p[0] = ExpressionLABEL('LABEL', p[1])


    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
    
    def run(self, code):
        self.parser.parse(code)