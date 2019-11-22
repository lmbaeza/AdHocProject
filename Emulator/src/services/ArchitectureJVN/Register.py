#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Register: <<clase Abstracta>>

class Register(object):

    def __init__(self):
        super().__init__()
    
    def getBinary(self):
        raise NotImplementedError

    def getNumber(self):
        raise NotImplementedError

# MICROSERVICIOS

# TODO:
# 1) Crear las clases 'DataRegister' que herede de la clase abstracta 'Register'
# 2) Agregar los atributos y Metodos
# class DataRegister(Register):

# TODO:
# 1) Crear las clases 'MicroInstructionRegister' que herede de la clase abstracta 'Register'
# 2) Agregar los atributos y Metodos
# class MicroInstructionRegister(Register):

# TODO:
# AX: Primary Accumulator
# 1) Crear las clases 'AX_Register' que herede de la clase 'DataRegister'
# 2) Agregar los atributos y Metodos
# class AX_Register(DataRegister):

# TODO:
# BX: Base Register
# 1) Crear las clases 'BX_Register' que herede de la clase 'DataRegister'
# 2) Agregar los atributos y Metodos
# class BX_Register(DataRegister):

# TODO:
# CX: Count Register
# 1) Crear las clases 'CX_Register' que herede de la clase 'DataRegister'
# 2) Agregar los atributos y Metodos
# class CX_Register(DataRegister):

# TODO:
# DX: Data Register
# 1) Crear las clases 'DX_Register' que herede de la clase 'DataRegister'
# 2) Agregar los atributos y Metodos
# class DX_Register(DataRegister):

# TODO:
# IR: Instruction Register
# 1) Crear las clases 'IR_Register' que herede de la clase 'DataRegister'
# 2) Agregar los atributos y Metodos
# class IR_Register(DataRegister):


# TODO:
# IP: Instruction Pointer
# 1) Crear las clases 'IP_Register' que herede de la clase 'MicroInstructionRegister'
# 2) Agregar los atributos y Metodos
# class IP_Register(MicroInstructionRegister):

