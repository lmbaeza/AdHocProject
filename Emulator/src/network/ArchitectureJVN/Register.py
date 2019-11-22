#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Register: <<clase Abstracta>>

class NodeRegister(object):

    def __init__(self):
        super().__init__()
    
    def getBinary(self):
        raise NotImplementedError

    def getNumber(self):
        raise NotImplementedError

# MICROSERVICIOS

# TODO:
# 1) Crear las clases 'NodeDataRegister' que herede de la clase abstracta 'NodeRegister'
# 2) Agregar los atributos y Metodos
# class NodeDataRegister(NodeRegister):

# TODO:
# 1) Crear las clases 'MicroInstructionRegister' que herede de la clase abstracta 'NodeRegister'
# 2) Agregar los atributos y Metodos
# class MicroInstructionRegister(NodeRegister):

# TODO:
# AX: Primary Accumulator
# 1) Crear las clases 'AX_Register' que herede de la clase 'NodeDataRegister'
# 2) Agregar los atributos y Metodos
# class A_Register(NodeDataRegister):

# TODO:
# BX: Base Register
# 1) Crear las clases 'B_Register' que herede de la clase 'NodeDataRegister'
# 2) Agregar los atributos y Metodos
# class B_Register(NodeDataRegister):

# TODO:
# CX: Count Register
# 1) Crear las clases 'C_Register' que herede de la clase 'NodeDataRegister'
# 2) Agregar los atributos y Metodos
# class C_Register(NodeDataRegister):

# TODO:
# DX: Data Register
# 1) Crear las clases 'D_Register' que herede de la clase 'NodeDataRegister'
# 2) Agregar los atributos y Metodos
# class D_Register(NodeDataRegister):

# TODO:
# IR: Instruction Register
# 1) Crear las clases 'IR_Register' que herede de la clase 'NodeDataRegister'
# 2) Agregar los atributos y Metodos
# class IR_Register(NodeDataRegister):


# TODO:
# IP: Instruction Pointer
# 1) Crear las clases 'IP_Register' que herede de la clase 'MicroInstructionRegister'
# 2) Agregar los atributos y Metodos
# class IP_Register(MicroInstructionRegister):