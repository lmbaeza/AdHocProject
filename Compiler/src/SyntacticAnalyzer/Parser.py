#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/dabeaz/ply/blob/master/ply/lex.py
# https://github.com/dabeaz/ply/blob/master/ply/yacc.py

from ply import yacc

from Compiler.src.LexicalAnalyzer.Scanner import Lexer

from Compiler.src.SemanticAnalyzer.SemanticAnalyzer import *
from Compiler.src.Exceptions.Exceptions import *
import random

class PythonDataType:
    # Variables Estaticas
    TYPE_INT = "<class 'int'>"
    TYPE_FLOAT = "<class 'float'>"
    TYPE_STR = "<class 'str'>"
    TYPE_BOOL = "<class 'bool'>"


class Parser(object):

    def __init__(self):
        # Tokens del Analizador Lexico
        self.tokens = Lexer().getToken()

        self.precedence = (
            ('left', 'PLUS', 'MINUS'),
            ('left', 'TIMES', 'DIVIDE'),
            ('right', 'UMINUS'),
        )

        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)


    # P_STATEMENT_ASSIGN

    def p_statement_list(self, p):
        r'''statements-list : statement statements-list
                            | expression_generic statements-list'''
        
        p[0] = StatementList(value=p[1], next=p[2])
    
    def p_statement_list_empty(self, p):
        r'''statements-list : '''


    # P_STATEMENT_FN_MAIN

    def p_statement_fn_main(self, p):
        r'''statement : FN MAIN LPAREN RPAREN LCURLY_BRACKET statements-list RCURLY_BRACKET'''

        next = p[6]

        while next is not None:
            tmp = next.evaluate()
            next = tmp


    # P_STATEMENT_IF
    def p_statement_if(self, p):
        r'''statement : IF LPAREN expression_generic RPAREN LCURLY_BRACKET statements-list RCURLY_BRACKET'''
        p[0] = StatementIf('If', p[3], p[6])


    # P_STATEMENT_IF_ELSE
    def p_statement_if_else(self, p):
        r'''statement : IF LPAREN expression_generic RPAREN LCURLY_BRACKET statements-list RCURLY_BRACKET ELSE LCURLY_BRACKET statements-list RCURLY_BRACKET'''
        p[0] = StatementIfElse('IfElse', p[3], p[6], p[10])
    

    def p_statement_assign_integer(self, p):
        r'''statement : INT ID EQUALS expression_integer SEMICOLON'''
        p[0] = StatementAssign('assign', 'INT', p, p[2], p[4])


    def p_statement_assign_float(self, p):
        r'''statement : DOUBLE ID EQUALS expression_float SEMICOLON'''
        p[0] = StatementAssign('assign', 'DOUBLE', p, p[2], p[4])


    def p_statement_assign_boolean(self, p):
        r'''statement : BOOLEAN ID EQUALS expression_boolean SEMICOLON'''
        p[0] = StatementAssign('assign', 'BOOLEAN', p, p[2], p[4])


    def p_statement_assign_string(self, p):
        r'''statement : STRING ID EQUALS expression_string SEMICOLON'''
        # p[0] = StatementAssign('assign', 'STRING', p, p[2], p[4])


    # P_STATEMENT_EXPR

    def p_statement_expr_generic(self, p):
        r'''statement : expression_generic SEMICOLON
                    | expression_generic'''
        
        # StatementExpr(p, p[1])


    # P_STATEMENT_UPDATE

    def p_statement_update_generic(self, p):
        r'''statement : ID UPDATE expression_generic SEMICOLON'''
        p[0] = StatementUpdate('Update', p, p[1], p[3])


    # P_EXPRESSION_BINOP

    def p_expression_binop_integer(self, p):
        r'''expression_integer : expression_integer PLUS expression_integer
                            | expression_integer MINUS expression_integer
                            | expression_integer TIMES expression_integer
                            | expression_integer DIVIDE expression_integer'''
        
        var = 'var'

        p[0] = ExpressionBinop('BinOp', p, var,  p[1], p[3], p[2])


    def p_expression_binop_float(self, p):
        r'''expression_float : expression_float PLUS expression_float
                    | expression_float MINUS expression_float
                    | expression_float TIMES expression_float
                    | expression_float DIVIDE expression_float'''

        var = 'var'

        p[0] = ExpressionBinop('BinOp', p, var,  p[1], p[3], p[2])


    # P_COMPARISON
    # https://stackoverflow.com/questions/47746590/python-ply-issue-with-if-else-and-while-statements

    def p_comparison_binop_integer(self, p):
        r'''comparison : expression_integer EQUAL expression_integer
                        | expression_integer NOTEQ expression_integer
                        | expression_integer LARGE expression_integer
                        | expression_integer LARGE_EQ expression_integer
                        | expression_integer SMALL expression_integer
                        | expression_integer SMALL_EQ expression_integer'''
        var = 'comp'
        p[0] = ComparisonBinop('ComparisonBinOp', p, var, p[1], p[3], p[2])
    

    def p_comparison_binop_float(self, p):
        r'''comparison : expression_float EQUAL expression_float
                        | expression_float NOTEQ expression_float
                        | expression_float LARGE expression_float
                        | expression_float LARGE_EQ expression_float
                        | expression_float SMALL expression_float
                        | expression_float SMALL_EQ expression_float'''

        # p[0] = ComparisonBinop(p, p[1], p[3], p[2])
    

    def p_comparison_binop_boolean(self, p):
        r'''comparison : expression_boolean EQUAL expression_boolean
                        | expression_boolean NOTEQ expression_boolean'''

        # p[0] = ComparisonBinop(p, p[1], p[3], p[2])
    

    def p_comparison_binop_string(self, p):
        r'''comparison : expression_string EQUAL expression_string
                        | expression_string NOTEQ expression_string
                        | expression_string LARGE expression_string
                        | expression_string LARGE_EQ expression_string
                        | expression_string SMALL expression_string
                        | expression_string SMALL_EQ expression_string'''

        # p[0] = ComparisonBinop(p, p[1], p[3], p[2])

    # P_EXPRESSION_UMINUS

    def p_expression_uminus_integer(self, p):
        r'''expression_integer : MINUS expression_integer %prec UMINUS'''
        p[0] = ExpressionUminus(p, p[2])


    def p_expression_uminus_float(self, p):
        r'''expression_float : MINUS expression_float %prec UMINUS'''
        p[0] = ExpressionUminus(p, p[2])


    # P_EXPRESSION_GROUP

    def p_expression_group_generic(self, p):
        '''expression_generic : LPAREN expression_generic RPAREN'''
        p[0] = ExpressionGroup(p, p[2])


    def p_expression_group_integer(self, p):
        '''expression_integer : LPAREN expression_integer RPAREN'''
        p[0] = ExpressionGroup(p, p[2])


    def p_expression_group_float(self, p):
        r'''expression_float : LPAREN expression_float RPAREN'''
        p[0] = ExpressionGroup(p, p[2])


    def p_expression_group_boolean(self, p):
        r'''expression_boolean : LPAREN expression_boolean RPAREN'''
        
        p[0] = ExpressionGroup(p, p[2])


    def p_expression_group_string(self, p):
        r'''expression_string : LPAREN expression_string RPAREN'''
        # p[0] = ExpressionGroup(p, p[2])


    # P_EXPRESSION

    def p_expression_integer_generic(self, p):
        r'''expression_generic : expression_integer
                                | expression_float
                                | expression_boolean
                                | expression_string'''
        p[0] = p[1]


    def p_expression_integer(self, p):
        r'''expression_integer : INTEGER'''
        p[0] = Integer(p[1])


    def p_expression_float(self, p):
        r'''expression_float : FLOAT'''
        p[0] = Float(p[1])


    def p_expression_boolean(self, p):
        r'''expression_boolean : BOOL'''
        p[0] = Boolean(p[1])


    def p_expression_string(self, p):
        r'''expression_string : STRING_CHAIN'''
        # p[0] = String(p[1])


    # P_EXPRESSION_ID

    def p_expression_id_generic(self, p):
        r'''expression_generic : ID'''
        p[0] = ExpressionID(p, p[1])


    def p_expression_id_integer(self, p):
        r'''expression_integer : ID'''
        p[0] = ExpressionID(p, p[1])


    def p_expression_id_float(self, p):
        r'''expression_float : ID'''
        p[0] = ExpressionID(p, p[1])


    def p_expression_id_boolean(self, p):
        r'''expression_boolean : ID'''
        p[0] = ExpressionID(p, p[1])


    def p_expression_id_string(self, p):
        r'''expression_string : ID'''
        # p[0] = ExpressionID(p, p[1])


    # P_EXPRESSION_COMPARISON

    def p_expression_comparison_to_boolean(self, p):
        r'''expression_boolean : comparison'''
        p[0] = p[1]


    # P_PRINT_ALL_TYPES

    def p_print_all_type(self, p):
        r'''statement : PRINT LPAREN expression_generic RPAREN SEMICOLON'''
        
        # Print(p, p[3])


    # P_PRINTLN_ALL_TYPES

    def p_println_all_type(self, p):
        r'''statement : PRINTLN LPAREN expression_generic RPAREN SEMICOLON
                        | PRINTLN LPAREN expression_generic RPAREN'''
        # Println(p, p[3])


    # P_EMPTY

    def p_empty(self, p):
        r'''statement : '''
        pass


    # P_ERROR

    def p_error(self, p):
        print(p)
        ErrorNotMatch(p)
    

    def shell(self):
        exit = False

        while not exit:
            try:
                s = input('shell> ')

                if s=='exit': break
            except EOFError:
                break
            self.parser.parse(s)


    def test(self, code):
        self.parser.parse(code)
