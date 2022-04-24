"""
Module containing exit codes and functions regarding them.
    
Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""

from ret_codes import *
import sys

class ArgumentProcessor:
    """Class for parsing command line arguments"""

    def __init__(self):
        """Parses arguments and prints help or saves input files paths into instance attributes"""
        self.source = None
        self.input = None
        
        self.statiFile = None
        self.stats = list()

        for arg in sys.argv[:]:
            if  arg in {"--insts", "--vars", "--hot"}:
                self.stats.append(arg[2:])
                sys.argv.remove(arg)
            elif arg.startswith("--stats="):
                self.statiFile = arg[8:]
                sys.argv.remove(arg)

        if self.stats and self.statiFile is None:
            self._paramErrExit()

        argc = len(sys.argv)
        if argc == 2:
            arg = sys.argv[1]
            if arg == "--help":
                self._printHelp()
                exit(SUCCES)
            elif arg.startswith("--source="):
                self.source = self._parseSource(arg)
            elif arg.startswith("--input="):
                self.input = self._parseInput(arg)
            else:
                self._paramErrExit()
        elif argc == 3:
            arg1 = sys.argv[1]
            arg2 = sys.argv[2]
            if arg1.startswith("--source=") and arg2.startswith("--input="):
                self.source = self._parseSource(arg1)
                self.input = self._parseInput(arg2)
            elif arg1.startswith("--input=") and arg2.startswith("--source="):
                self.input = self._parseInput(arg1)
                self.source = self._parseSource(arg2)
            else:
                self._paramErrExit()

        else:
            self._paramErrExit()

    @staticmethod
    def _printHelp():
        print("Usage: python3.8 interpret.py")
        print("Loads XML representation of an IPPcode2022 program,", end='') 
        print("interprets this program and generates output.\n")
        print(" --source=file   source file with program XML repreesntation")
        print(" --input=file    file with input for the interpretation itself")
        print("  One of these parameters has to be present.")
        print("  If file parameter missing, standard input is used instead of it")

    @staticmethod
    def _parseSource(source):
        """Parses --source=file parameter and returns only file"""
        return source[9:]

    @staticmethod
    def _parseInput(input):
        """Parses --input=file parameter and returns only file"""
        return input[8:]

    @staticmethod
    def _paramErrExit():
        """Prints wrong params error to stderr and exits with corresponing code"""
        exitWMsg(PARAMETER_ERR, "Unsupported combination of program arguments")