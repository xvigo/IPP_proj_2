"""
Module containing IPPcode2022 data types.
    
Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""
from enum import Enum
from ret_codes import *
from frames import *
from re import sub, match

class ConstantType(Enum):
    """Enum representing constant value type."""
    INT = 0
    STRING = 1
    BOOL = 2
    NIL = 3
    FLOAT = 4

    @staticmethod
    def parse(typeString):
        """Converts string marking type to corresponding ConstantType."""
        if typeString == "int":
            return ConstantType.INT
        elif typeString == "bool":
            return ConstantType.BOOL
        elif typeString == "nil":
            return ConstantType.NIL
        elif typeString == "float":
            return ConstantType.FLOAT
        else:
            return ConstantType.STRING


class Symb:
    """Symbol data type (variable, or constant."""

    def getConst(self):
        """Returns constant contained in a symbol."""
        if isinstance(self, Variable):
            return self.getValue()
        else: #src is constant
            return self

    def getTypeString(self):
        """Returns type of symbol for use in WRITE instruction."""
        if isinstance(self, Variable):
            const =  self.getValueUninit()
        else: #already constant
            const = self
        
        if const is None:
            return ""
        elif const.type is ConstantType.STRING:
            return "string"
        elif const.type is ConstantType.BOOL:
            return "bool"
        elif const.type is ConstantType.INT:
            return "int"
        elif const.type is ConstantType.FLOAT:
            return "float"
        else:
            return "nil"


class Constant(Symb):
    """Symbol data type containing value type and value attributes."""

    def __init__(self, constType, value):
        """Create new constant with given type and value."""
        self.type = constType
        self.value = value
    
    @staticmethod
    def expandEcsSeq(matchObj):
        """Expands string escape sequences to characters"""
        char = chr(int(matchObj.group(1)))
        return char

    def toString(self):
        """Convert constant value to string."""
        if self.type is ConstantType.STRING:
            return self.value
        elif self.type is ConstantType.INT:
            return str(self.value)
        elif self.type is ConstantType.FLOAT:
            return float.hex(self.value)
        elif self.type is ConstantType.BOOL:
            if self.value is True:
                return "true"
            else:   
                return "false"
        else: # ConstantType.NIL
            return ""

    @staticmethod
    def parseFromStrXml(constTypeStr, string):
        """Creates new constant based on given string values from input XML."""
        type = ConstantType.parse(constTypeStr)

        if type is ConstantType.INT:
            value = int(string)
        elif type is ConstantType.FLOAT:
            try: 
                value = float(string)
            except ValueError:
                value = float.fromhex(string)
        elif type is ConstantType.BOOL:
            if string == "true":
                value = True
            else:
                value = False
        elif type is ConstantType.NIL:
            value = None
        else:
            if string is None:
                value = ""
            else:
                value = sub(r"\\(\d{3})", Constant.expandEcsSeq, string)

        return Constant(type, value)


    @staticmethod
    def parseFromStrInput(constType, string):
        """Creates new constant based on given string values from interpret input."""
        if constType is ConstantType.INT:
            try:
                value = int(string)
            except ValueError:
                try:
                    value = float(string)
                except ValueError:
                    try:
                        value = float.fromhex(string)
                    except ValueError:
                        value = None
                        constType = ConstantType.NIL
            if isinstance(value, float):
                value = int(value)
        elif constType is ConstantType.FLOAT:
            try: 
                value = float(string)
            except ValueError:
                try:
                    value = float.fromhex(string)
                except ValueError:
                    value = None
                    constType = ConstantType.NIL

        elif constType is ConstantType.BOOL:
            if string.lower() == "true":
                value = True
            else:
                value = False
        else:
            if string == "":
                value = None
                constType = ConstantType.NIL
            else:
                value = sub(r"\\(\d{3})", Constant.expandEcsSeq, string)

        return Constant(constType, value)

    @staticmethod
    def checkTypes(type, operand1, operand2):
        """Checks whether whether both operands are given type.
        If not, prints wrong operands types error and exits program"""
        if operand1.type is not type or operand2.type is not type:
            exitWMsg(RUN_OPERANDS_ERR, "Wrong operand types")

    @staticmethod
    def checkNumericTypes(operand1, operand2):
        """Checks whether whether both operands are the same numeric type and return it.
        If not, prints wrong operands types error and exits program"""
        if operand1.type is ConstantType.FLOAT and operand2.type is ConstantType.FLOAT:
            return ConstantType.FLOAT
        elif operand1.type is ConstantType.INT and operand2.type is ConstantType.INT:
            return ConstantType.INT
        else:
            exitWMsg(RUN_OPERANDS_ERR, "Wrong operand types")

    @staticmethod
    def checkSameTypes(operand1, operand2):
        """Checks whether whether operands are the same type.
        If not, prints wrong operands types error and exits program"""
        if operand1.type is not operand2.type :
            exitWMsg(RUN_OPERANDS_ERR, "Wrong operand types")

class Variable(Symb):
    """Variable data type located in a frame"""
    def __init__(self, name):
        """Creates new variable in frame based on its name"""
        self.name = name[3:]
        self.frame = Frame.parse(name)

    def getValue(self):
        """Get variable value, if its initialized, otherwise error"""
        return self.frame.getVar(self.name)

    def getValueUninit(self):
        """Get variable value, even if its uninitialized"""
        return self.frame.getVar(self.name, hasToBeInit = False)

    def updateValue(self, value):
        """Change value of given variable to given value"""
        self.frame.updateVar(self.name, value)
    
    def define(self):
        """Defines new variable that is uninitialised"""
        self.frame.defVar(self.name)

class LabelNT:
    """Label non-terminal data type;"""
    def __init__(self, name):
        """Create new label with given name"""
        self.name = name