"""
Module containing exit codes and function regarding them.
    
Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""

from sys import stderr

# -- general -- 
SUCCES = 0
PARAMETER_ERR = 10 
"""Missing script parameter or invalid combination of parameters"""

INPUT_FILE_ERR = 11 
"""Error while opening input file"""

OUTPUT_FILE_ERR = 12
"""Error while opening output file"""

INTERNAL_ERR = 99 
"""Internal error (e.g. memmory error)"""

# -- interpret specific -- 
# input xml
XML_FORMAT_ERR = 31
"""Input XML isn't well formed"""

XML_STRUCTURE_ERR = 32 
"""Unexpected strucutre of XML"""

# runtime
RUN_SEMANTIC_ERR = 52
"""Undefined label, variable redefinition """

RUN_OPERANDS_ERR = 53 
"""Invalid operand types"""

RUN_VAR_EXIST_ERR = 54
"""Accessing nonexistent variable"""

RUN_FRAME_EXIST_ERR = 55 
"""Nonexistent frame (reading from empty frame stack)"""

RUN_VAL_MISSING_ERR = 56 
"""Missing value (variable, data stack, call stack)"""

RUN_VAL_WORNG_ERR = 57 
"""Invalid operand value (zero division, invalid EXIT value)"""

RUN_STR_ERR = 58 
"""Invalid string operation"""

def exitWMsg(exitCode, *message):
        """Print message to stderr and exit program with given code."""
        print("ERROR -", *message, file = stderr)
        exit(exitCode)