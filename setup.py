import sys
import os
from cx_Freeze import setup, Executable

# Must copy tcl86t.dll and tk86t.dll into build folder
os.environ['TCL_LIBRARY'] = "C:\\Users\\zdrazil\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\zdrazil\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"


# executables = [
#     Executable('filter_cz.py')
# ]
#
# setup(name='Filter CZ payments',
#       version='0.1',
#       description='Filters czech payments in csv to txt',
#       executables=executables, requires=['pandas']
#       )

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('gui.py', base=base)
]

build_exe_options = {"include_files": ["tcl86t.dll", "tk86t.dll"], 
					 "packages": ['pandas','numpy']
}  


setup(name='Filtr Plateb',
      version='0.1',
      description='Filter payments',
      options={"build_exe": build_exe_options},  
	  executables=executables,
      requires=[
          'pandas', 'numpy'
      ]
      )

# executables=executables, requires=['pandas']