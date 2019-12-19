#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Compiler.src.GUI.windows import Windows
from tkinter import *


tk = Tk()
windows = Windows(tk)
tk.resizable(0,0)
tk.mainloop()