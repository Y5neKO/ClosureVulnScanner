import os
import sys
import win32con
import win32api
from tkinter import *

root = Tk()
root.resizable(width=False, height=False)
text = Text(root)
text.pack(fill=X, side=BOTTOM)
text.grid(row=0, padx=2, pady=2)

mainloop()
