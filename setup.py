import sys 
from cx_Freeze import setup, Executable 

setup(name = 'Project', 
      version = '0.1', 
      description = 'SQL', 
      executables = [Executable("Test.py")])