#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RAM_Node(object):

    def __init__(self, size=1024):
        self.memory = []
        self.virtualMemory = []

        for i in range(0, size):
            self.memory.append(None)
            self.virtualMemory.append(False)

    def getAddress(self, address):
        return self.memory[address]
    
    def setAddress(self, cell, address):
        # TODO: Implementar este metodo
        pass

    def free(self, address):
        # TODO: Implementar este metodo
        pass

    def isFree(self, address):
        # TODO: Implementar este metodo
        pass

