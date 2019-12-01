#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ply import yacc

from Compiler.src.Assembler.LexASM import LexerASM


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

    def p_statement_list(self, p):
        r'''statements-list : statement statements-list'''
        pass
    
    def p_statement_list_empty(self, p):
        r'''statements-list : '''
        pass

    
    def p_statement_assign(self, p):
        r'statement : ID EQUALS expression'

        print(list(p))

    def p_statement_assign_tmp(self, p):
        r'statement : TMP EQUALS expression'

        print(list(p))

    def p_statement_expr(self, p):
        r'statement : expression'
        print(list(p))
    
    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
        print(list(p))
        
        if p[2] == '+':
            p[0] = str(p[1]) + ' + '  + str(p[3])
        elif p[2] == '-':
            p[0] = str(p[1]) + ' - '  + str(p[3])
        elif p[2] == '*':
            p[0] = str(p[1]) + ' * '  + str(p[3])
        elif p[2] == '/':
            p[0] = str(p[1]) + ' / '  + str(p[3])
    
    def p_expression_comparison(self, p):
        r'expression : expression EQUAL expression'
        p[0] = str(p[1]) + ' == ' + str(p[3])
        print(list(p))

    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        print(list(p))
        p[0] = -p[2]
    

    def p_expression_integer(self, p):
        "expression : INTEGER"
        print(list(p))
        p[0] = p[1]


    def p_expression_float(self, p):
        "expression : FLOAT"
        print(list(p))
        p[0] = p[1]


    def p_expression_name(self, p):
        "expression : ID"
        print(list(p))
        p[0] = p[1]
        # try:
        #     p[0] = names[p[1]]
        # except LookupError:
        #     print("Undefined name '%s'" % p[1])
        #     p[0] = 0

    def p_expression_tmp(self, p):
        "expression : TMP"
        print(list(p))
        p[0] = p[1]

    def p_expression_ifnot(self, p):
        r'''expression : IFNOT TMP GOTO LABEL
                       | IFNOT ID GOTO LABEL'''
        print(list(p))
    
    def p_expression_goto(self, p):
        r'expression : GOTO LABEL'
        print(list(p))

    def p_expression_label(self, p):
        r'expression : LABEL'
        print(list(p))


    def p_error(self, p):
        if p:
            # print(list(p))
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
    
    def run(self, code):
        self.parser.parse(code)