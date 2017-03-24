import sys
import os
from cx_Freeze import setup, Executable

# Must copy tcl86t.dll and tk86t.dll into build folder
os.environ['TCL_LIBRARY'] = "C:\\Users\\zdrazil\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\zdrazil\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6"


executables = [
    Executable('filter_cz.py')
]

setup(name='Filter CZ payments',
      version='0.1',
      description='Filters czech payments in csv to txt',
      executables=executables
      )
