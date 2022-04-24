"""
Module containing variable frames.
    
Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""

from ast import Constant
from ret_codes import *
from stack import Stack
class Frame:
    """Generic frame implementing common methods for further inheritance."""
    @classmethod
    def defVar(cls, name):
        """Define new variable in a frame."""
        if not cls.frameDefined():
            cls._exitAcessNonexFrame()
            
        if cls.varDefined(name):
            cls._exitRedefinition(name)

        cls._setVal(name, None)
    
    @classmethod
    def updateVar(cls, name, const):
        """Update variable value in a frame."""
        if not cls.frameDefined():
            cls._exitAcessNonexFrame()

        if not cls.varDefined(name):
            cls._exitAcessNonexist(name)

        cls._setVal(name, const)

    @classmethod
    def getVar(cls, name, hasToBeInit = True):
        """Get variable value from frame."""
        if not cls.frameDefined():
            cls._exitAcessNonexFrame()

        if not cls.varDefined(name):
            cls._exitAcessNonexist(name)

        if hasToBeInit:
            if not cls.varInitialised(name):
                cls._exitAcessUninit(name)

        return cls._getVal(name)
    
    @classmethod
    def frameDefined(cls):
        """Returns bool whether frame is defined."""
        return cls._vars is not None

    @classmethod
    def varDefined(cls, name):
        """Returns bool whether given variable was defined in a frame."""
        return name in cls._vars
         
    @classmethod
    def varInitialised(cls, name):
        """Returns bool whether given variable was initialised in a frame."""
        return cls._getVal(name) is not None

    @classmethod
    def _getVal(cls, name):
        """Private variable getter."""
        return cls._vars[name]
   
    @classmethod       
    def _setVal(cls, name, value):
        """Private variable setter."""
        cls._vars[name] = value

    @classmethod       
    def getInitCount(cls):
        """Get number of initialized variables in a frame."""
        if not cls.frameDefined():
            return 0

        count = 0
        for value in cls._vars.values():
            if value is not None:
                count += 1

        return count

    @staticmethod
    def _exitRedefinition(varName):
        """Print variable redefinition error to stderr and exits program."""
        exitWMsg(RUN_SEMANTIC_ERR, "Variable redefinition, name:", varName)

    @staticmethod
    def _exitAcessNonexist(varName):
        """Print accesing nonexistent variable error and exits program."""
        exitWMsg(RUN_VAR_EXIST_ERR, "Acessing nonexistent variable, name:", varName)

    @staticmethod
    def _exitAcessUninit(varName):
        """Print accesing uninitialised variable error and exits program."""
        exitWMsg(RUN_VAL_MISSING_ERR, "Acessing uninitialized variable, name:", varName)

    @staticmethod
    def _exitAcessNonexFrame():
        """Print accesing undefined frame error and exits program."""
        exitWMsg(RUN_FRAME_EXIST_ERR, "Acessing undefined frame")
    
    @staticmethod
    def parse(varString):
        """Converts string marking frame type to corresponding class."""
        if varString.startswith("LF"):
            return LocFrame
        elif varString.startswith("GF"):
            return GlobFrame
        elif varString.startswith("TF"):
            return TempFrame

class GlobFrame(Frame):
    """Global frame with single frame."""
    _vars = dict()

class LocFrame(Frame):
    """"Local frame with single frame and frame stack."""
    _vars = None
    _stack = Stack()

    @classmethod
    def pushFrame(cls):
        """Push frame into frame stack."""
        if not TempFrame.frameDefined():
            cls._exitAcessNonexFrame()

        cls._stack.push(TempFrame._vars)
        cls._vars = cls._stack.top()
        TempFrame.undefFrame()

    @classmethod
    def popFrame(cls):
        """Remove frame from frame stack and return it."""
        if cls._stack.isEmpty():
            cls._exitAcessNonexFrame()

        TempFrame._vars = cls._stack.pop()

        if cls._stack.isEmpty():
            cls._vars = None
        else:
            cls._vars = cls._stack.top()


class TempFrame(Frame):
    """"Temporary frame with single frame that has to be explicitly defined"""
    _vars = None

    @classmethod    
    def createFrame(cls):
        """Creates new frame"""
        cls._vars = dict()
    
    @classmethod
    def undefFrame(cls):
        """Undefines existing frame"""
        cls._vars = None