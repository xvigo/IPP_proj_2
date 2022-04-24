"""
Module containing classes representing IPPcode2022 Program and its individual Instructions
and minor program components.
    
Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""

import xml.etree.ElementTree as ET
import importlib
from re import match
import sys

from frames import *
from data_types import *
from stack import Stack


class Stats:
    """Stati extension stats counter."""
    def __init__(self):
        self.insts = 0
        self.hot = dict()
        self.vars = 0
        self.config = None
        self.file = None
    
    def countIn(self, instruction):
        """ Count instruction into statistics."""
        if not self.isActivated():
            return

        if  isinstance(instruction, (Label, Dprint, Break)):
            return
        
        self.addExecInst()
        self.addHot(instruction.order)
        self.assignVars()

    def addExecInst(self):
        """Counts in executed instruction."""
        self.insts += 1

    def addHot(self, order):
        """Adds instruction order into hot counter."""
        hotVal = self.hot.get(order, 0)
        self.hot.update({order:hotVal + 1}) 

    def getHottest(self):
        """Get instruction with most occurences."""
        hotList = list(self.hot.items())
        hotList.sort(key = lambda a: a[0]) # sort by insrt order
        hottest = max(hotList, key = lambda a: a[1])[0] # get with most occurencces
        return hottest

    def assignVars(self):
        """Assign new max number of initialised variables."""
        sum = LocFrame.getInitCount() + GlobFrame.getInitCount() + TempFrame.getInitCount()
        if sum > self.vars:
            self.vars = sum
    
    def addConfig(self, config):
        """Adds new tests config."""
        self.config = config

    def addFile(self, file):
        """Adds new tests output file."""
        self.file = file

    def isActivated(self):
        """Returns bool whether stats are activated"""
        return self.file is not None

    def printStats(self):
        """Prints stats into output file given in config."""
        if not self.isActivated():
            return

        output = ""
        for statName in self.config:
            if statName == "insts":
                output += str(self.insts)
            elif statName == "hot":
                output += str(self.getHottest()) 
            elif statName == "vars":
                output += str(self.vars)
            output += "\n"

        try:
             f = open(self.file, "w")
        except IOError:
            exitWMsg(OUTPUT_FILE_ERR, "Could not creat STATI output file.")
        f.write(output)
        f.close()
        
class ProgramCounter:
    """Program counter marking current instruction index"""
    def __init__(self):
        self.idx = 0
        self.jump = False
    
    def next(self):
        """Increment program counter instruction index"""
        self.idx += 1
    
    def jumpTo(self, index):
        """Change program counter due to jump to instruction with given index"""
        self.idx = index
        self.jump = True
    
    def getIndex(self):
        """Get program counter instruction index"""
        return self.idx

class ReadInput:
    """Interpret input for READ instruction"""
    def __init__(self, file):
        """Creates new Read input based on given file.
        
        If no file - input is read from standard input,
        otherwise input is read from given file"""
        if file is None:
            self.lines = None
        else:
            try:
                with open(file) as f:
                    self.lines = f.readlines()
            except OSError:
                exitWMsg(INPUT_FILE_ERR, "Couldn't open input file for READ instructions")

    def getLine(self):
        """Get line from interpret input file."""
        if self.lines is None:
            try:
                string = input()
            except EOFError:
                string = ""
        else:
            try:
                string = self.lines.pop(0)
            except IndexError:
                string = ""

        return string

class Program:
    """Class representing IPPcode22 program."""
    counter = ProgramCounter()

    callStack = Stack()
    dataStack = Stack()

    stats = Stats()

    @classmethod
    def load(cls, source):
        """Loads program from given input XML file."""
        if source is None:
            source = sys.stdin
        cls._getXmlTree(source)
        cls._xmlTreeParse()
        cls._sortInstructions()
        cls._setLabels()
        cls._addTerminatingInstruction()

    @classmethod
    def _getXmlTree(cls, sourceFile):
        """Gets XML tree representation from input XML file."""
        try:
            cls.xmlTree = ET.parse(sourceFile)
        except ET.ParseError:
            exitWMsg(XML_FORMAT_ERR, "Input xml is not well-formed")
        except OSError:
            exitWMsg(INPUT_FILE_ERR, "Couldn't open XML program source file")

    @classmethod
    def _xmlTreeParse(cls):
        """Parses XML tree into instructions and their arguments"""
        cls.instructions = list()
        root = cls.xmlTree.getroot()

        if root.tag != "program":
            exitWMsg(XML_STRUCTURE_ERR, "Missing program tag in source XML")
        
        language = root.attrib.get("language")
        if language is None:
            exitWMsg(XML_STRUCTURE_ERR, "Missing language attribute in source XML program tag")
        if language != "IPPcode22":
            exitWMsg(XML_STRUCTURE_ERR, "Unsupported language in source XML program tag")

        for instrTag in root:
            if instrTag.tag != "instruction":
                exitWMsg(XML_STRUCTURE_ERR, "Unexpected tag in source XML:", instrTag.tag)

            opcode = instrTag.attrib.get("opcode")
            if opcode is None:
                exitWMsg(XML_STRUCTURE_ERR, "Missing opcode attribute in source XML instruction tag")
            try:
                instrClass = getattr(importlib.import_module("program"), opcode.capitalize())
            except AttributeError:
                exitWMsg(XML_STRUCTURE_ERR, "Unsuported opcode in source XML instruction tag:", opcode)


            instruction = instrClass(instrTag)
            cls.instructions.append(instruction)

    @classmethod
    def _sortInstructions(cls):
        """Sorts instructions by their order attribure in ascending order."""
        cls.instructions.sort(key = lambda a: a.order)

    @classmethod
    def _setLabels(cls):
        """Assings labels instructions their jump indexes."""
        for i in range(len(cls.instructions)):
            instruction = cls.instructions[i]
            if instruction.isType(Label):
                labelNT = instruction.getNT()
                Label.updateInstrIdx(labelNT, i)

    @classmethod
    def _addTerminatingInstruction(cls):
        """Adds program end marking instruction."""
        cls.instructions.append(None)

    @classmethod
    def interpret(cls, source, statsConf, statFile):
        """Interprets program instructions loaded in class."""
        cls.readInput = ReadInput(source)
        cls.stats.addConfig(statsConf)
        cls.stats.addFile(statFile)

        while cls.instructions[cls.counter.getIndex()] is not None:
            instr = cls.instructions[cls.counter.getIndex()]
            try:
                instr.exec()
            except IndexError:
                exitWMsg(XML_STRUCTURE_ERR, "Missinng arg tag in source XML instruction tag")

            cls.stats.countIn(instr)

            if cls.counter.jump:
                cls.counter.jump = False
            else:
                cls.counter.next()
            
        cls.stats.printStats()
        
class Instruction:
    """General IPPcode22 instruction for further inheritance."""
    orders = set()

    def __init__(self, instrTag):
        """Create new instuction based on given XML instruction tag"""
        order = instrTag.attrib.get("order")
        if order is None:
            exitWMsg(XML_STRUCTURE_ERR, "Missinng order attribute in source XML instruction tag")

        try:
            order = int(order)
            if order < 0:
                raise ValueError
        except ValueError:
            exitWMsg(XML_STRUCTURE_ERR, "Instruction order in input XML has unsupported value:", order)

        if order in Instruction.orders:
            exitWMsg(XML_STRUCTURE_ERR, "Duplicit instruction order in input XML instruction tags, value:", order)
        
        self.order = order
        Instruction.orders.add(order)

        self.args = list()
        index = 1
        for argTag in instrTag:
            arg = self._parseArgTag(argTag, index)
            self.args.append(arg)
            index += 1

    @staticmethod         
    def _parseArgTag(argTag, index):
        """Parses XML instruction argument tag and returns its data type representation"""
        if not match(f"^arg{index}$",argTag.tag):
            exitWMsg(XML_STRUCTURE_ERR, "Unexpected tag in source XML, value:", argTag.tag)

        argType = argTag.attrib.get("type")
        if argType == "label":
            return LabelNT(argTag.text)
        elif argType == "var":
            return Variable(argTag.text)
        elif argType == "type":
            return ConstantType.parse(argTag.text)
        else:
            return Constant.parseFromStrXml(argType, argTag.text)

    def isType(self, InstructionType):
        return isinstance(self, InstructionType)


# --- Classes for each instruction -----
# Class names are equivalent to instructions opcodes
# - exec: method simulating instruction execution - interprets it

class Move(Instruction):
    def exec(self):
        destVar = self.args[0]
        srcSymb = self.args[1]
        
        value = srcSymb.getConst()

        destVar.updateValue(value)

class Createframe(Instruction):
    def exec(self):
        TempFrame.createFrame()

class Pushframe(Instruction):
    def exec(self):
        LocFrame.pushFrame()

class Popframe(Instruction):
    def exec(self):
        LocFrame.popFrame()

class Defvar(Instruction):
    def exec(self):
        var = self.args[0]
        var.define()

class Call(Instruction):
    def exec(self):
        labelNT = self.args[0]

        nextInstrIdx = Program.counter.getIndex() + 1
        Program.callStack.push(nextInstrIdx)

        jumpIndex = Label.getInstrIdx(labelNT)
        Program.counter.jumpTo(jumpIndex)

class Return(Instruction):
    def exec(self):        
        if Program.callStack.isEmpty():
            exitWMsg(RUN_VAL_MISSING_ERR, "'RETURN' instruction without previous 'CALL' instruction")

        idx = Program.callStack.pop()
        Program.counter.jumpTo(idx)

class Pushs(Instruction):
    def exec(self):
        symb = self.args[0]
        const = symb.getConst()
        Program.dataStack.push(const)

class Pops(Instruction):
    def exec(self):
        destVar = self.args[0]

        if Program.dataStack.isEmpty():
            exitWMsg(RUN_VAL_MISSING_ERR, "'POPS' - pop on empty data stack")

        const = Program.dataStack.pop()
        destVar.updateValue(const)

class Add(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        ConType = Constant.checkNumericTypes(const1, const2)
        result = const1.value + const2.value
        destVar.updateValue(Constant(ConType, result))

class Sub(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        ConType = Constant.checkNumericTypes(const1, const2)
        result = const1.value - const2.value
        destVar.updateValue(Constant(ConType, result))

class Mul(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        ConType = Constant.checkNumericTypes(const1, const2)
        result = const1.value * const2.value
        destVar.updateValue(Constant(ConType, result))

class Idiv(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        if const2.value == 0:
            exitWMsg(RUN_VAL_WORNG_ERR, "Division by zero")

        Constant.checkTypes(ConstantType.INT, const1, const2)
        result = const1.value // const2.value
        destVar.updateValue(Constant(ConstantType.INT, result))

class Div(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        if const2.value == 0:
            exitWMsg(RUN_VAL_WORNG_ERR, "Division by zero")

        Constant.checkTypes(ConstantType.FLOAT, const1, const2)
        result = const1.value / const2.value
        destVar.updateValue(Constant(ConstantType.FLOAT, result))

class Lt(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        if (const1.type is ConstantType.NIL or const2.type is ConstantType.NIL):
            exitWMsg(RUN_OPERANDS_ERR, "Wrong operands type, 'nil' can be compared only with 'EQ'")
        
        Constant.checkSameTypes(const1, const2)
        result = const1.value < const2.value
        destVar.updateValue(Constant(ConstantType.BOOL, result))

class Gt(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        if (const1.type is ConstantType.NIL or const2.type is ConstantType.NIL):
            exitWMsg(RUN_OPERANDS_ERR, "Wrong operands type, 'nil' can be compared only with 'EQ'")
        
        Constant.checkSameTypes(const1, const2)
        result = const1.value > const2.value
        destVar.updateValue(Constant(ConstantType.BOOL, result))

class Eq(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()

        if const1.type is ConstantType.NIL and const2.type is ConstantType.NIL:
            result = True
        elif const1.type is ConstantType.NIL or const2.type is ConstantType.NIL:
            result = False
        else:
            Constant.checkSameTypes(const1, const2)
            result = (const1.value == const2.value)
        
        destVar.updateValue(Constant(ConstantType.BOOL, result))

class And(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()
        
        Constant.checkTypes(ConstantType.BOOL, const1, const2)
        result = const1.value and const2.value
        destVar.updateValue(Constant(ConstantType.BOOL, result))

class Or(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()
        
        Constant.checkTypes(ConstantType.BOOL, const1, const2)
        result = const1.value or const2.value
        destVar.updateValue(Constant(ConstantType.BOOL, result))

class Not(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()
        
        if const1.type != ConstantType.BOOL:
            exitWMsg(RUN_OPERANDS_ERR, "NOT: operator has to be bool type")
        result = not const1.value
        destVar.updateValue(Constant(ConstantType.BOOL, result))

class Int2char(Instruction):
    def exec(self):
        destVar = self.args[0]
        const1 = self.args[1].getConst()

        if const1.type is not ConstantType.INT:
            exitWMsg(RUN_OPERANDS_ERR, "INT2CHAR: wrong operand type - operand has to be int")

        try:
            result = chr(const1.value)
        except ValueError:
            exitWMsg(RUN_STR_ERR, "INT2CHAR: int value ins't valid UNICODE value")
        destVar.updateValue(Constant(ConstantType.STRING, result))

class Stri2int(Instruction):
    def exec(self):
        destVar = self.args[0]
        string = self.args[1].getConst()
        index = self.args[2].getConst()

        if string.type is not ConstantType.STRING or index.type is not ConstantType.INT:
            exitWMsg(RUN_OPERANDS_ERR, "STR2INT: wrong operand types")

        if index.value >= len(string.value) or index.value < 0:
            exitWMsg(RUN_STR_ERR, "STR2INT: string index out of range")

        result = ord(string.value[index.value])
        destVar.updateValue(Constant(ConstantType.INT, result))

class Int2float(Instruction):
    def exec(self):
        destVar = self.args[0]
        const = self.args[1].getConst()

        if const.type is not ConstantType.INT:
            exitWMsg(RUN_OPERANDS_ERR, "INT2FLOAT: wrong operand type - operand has to be int")

        result = float(const.value)
        destVar.updateValue(Constant(ConstantType.FLOAT, result))

class Float2int(Instruction):
    def exec(self):
        destVar = self.args[0]
        const = self.args[1].getConst()

        if const.type is not ConstantType.FLOAT:
            exitWMsg(RUN_OPERANDS_ERR, "FLOAT2INT: wrong operand type - operand has to be float")

        result = int(const.value)
        destVar.updateValue(Constant(ConstantType.INT, result))

class Read(Instruction):
    def exec(self):
        destVar = self.args[0]
        constType = self.args[1]
        
        string = Program.readInput.getLine()
        if len(string) != 0 and string[-1] == '\n':
            string = string[:-1]
        constant = Constant.parseFromStrInput(constType, string)
        destVar.updateValue(constant)

class Write(Instruction):
    def exec(self):
        symb = self.args[0]
        const = symb.getConst()

        valueString = const.toString()

        print(valueString, end='')

class Concat(Instruction):
    def exec(self):
        destVar = self.args[0]
        str1 = self.args[1].getConst()
        str2 = self.args[2].getConst()
        
        Constant.checkTypes(ConstantType.STRING, str1, str2)

        result = str1.value + str2.value
        destVar.updateValue(Constant(ConstantType.STRING, result))

class Strlen(Instruction):
    def exec(self):
        destVar = self.args[0]
        str1 = self.args[1].getConst()

        if str1.type is not ConstantType.STRING:
            exitWMsg(RUN_OPERANDS_ERR, "STRLEN: operand has to be string")

        result = len(str1.value)
        destVar.updateValue(Constant(ConstantType.INT, result))

class Getchar(Instruction):
    def exec(self):
        destVar = self.args[0]
        string = self.args[1].getConst()
        index = self.args[2].getConst()

        if string.type is not ConstantType.STRING or index.type is not ConstantType.INT:
            exitWMsg(RUN_OPERANDS_ERR, "GETCHAR: wrong operand types")

        if index.value >= len(string.value) or index.value < 0:
            exitWMsg(RUN_STR_ERR, "GETCHAR: string index out of range")

        result = string.value[index.value]
        destVar.updateValue(Constant(ConstantType.STRING, result))

class Setchar(Instruction):
    def exec(self):
        destVar = self.args[0]
        destString = destVar.getConst()
        index = self.args[1].getConst()
        srcString = self.args[2].getConst()

        if index.type is not ConstantType.INT:
            exitWMsg(RUN_OPERANDS_ERR, "SETCHAR: index has to be int value")

        Constant.checkTypes(ConstantType.STRING, destString, srcString)

        if index.value >= len(destString.value) or index.value < 0:
            exitWMsg(RUN_STR_ERR, "SETCHAR: string index out of range")
        
        if len(srcString.value) <= 0:
            exitWMsg(RUN_STR_ERR, "SETCHAR: source string is empty")

        newChar = srcString.value[0]
        result = destString.value[:index.value] + newChar + destString.value[index.value + 1:]
        destVar.updateValue(Constant(ConstantType.STRING, result))

class Type(Instruction):
    def exec(self):
        destVar = self.args[0]
        symbTypeStr = self.args[1].getTypeString()

        destVar.updateValue(Constant(ConstantType.STRING, symbTypeStr))

class Label(Instruction):
    """Label instruction class containing labels jump indexes."""
    _definedLabels = dict()

    def __init__(self, instrTag):
        """"""
        super().__init__(instrTag)
        labelName = self.args[0].name
        if  labelName in Label._definedLabels:
            exitWMsg(RUN_SEMANTIC_ERR, "Label redefinition, name:", labelName)

        Label._definedLabels[labelName] = None

    def exec(self):
        pass

    def getNT(self):
        """Get label instruction label nonterminal."""
        return self.args[0]

    @classmethod
    def getInstrIdx(cls, labelNT):
        """Get instruction index of given label nonterminal"""
        labelName = labelNT.name
        if labelName not in cls._definedLabels:
            exitWMsg(RUN_SEMANTIC_ERR, "Jump to unexistent label, name:", labelName)

        return cls._definedLabels[labelName]
    
    @classmethod
    def updateInstrIdx(cls, labelNT, index):
        """Change instruction index of given label to given value."""
        cls._definedLabels[labelNT.name] = index
    
class Jump(Instruction):
    def exec(self):
        labelName = self.args[0]

        jumpIndex = Label.getInstrIdx(labelName)
        Program.counter.jumpTo(jumpIndex)


class Jumpifeq(Instruction):
    def exec(self):
        labelName = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()
        jumpIndex = Label.getInstrIdx(labelName)

        
        if const1.type is ConstantType.NIL and const2.type is ConstantType.NIL:
            jump = True
        elif const1.type is ConstantType.NIL or const2.type is ConstantType.NIL:
            jump = False
        else:
            Constant.checkSameTypes(const1, const2)
            jump = (const1.value == const2.value)

        if jump:
            Program.counter.jumpTo(jumpIndex)


class Jumpifneq(Instruction):
    def exec(self):
        labelName = self.args[0]
        const1 = self.args[1].getConst()
        const2 = self.args[2].getConst()
        jumpIndex = Label.getInstrIdx(labelName)

        if const1.type is ConstantType.NIL and const2.type is ConstantType.NIL:
            jump = False
        elif const1.type is ConstantType.NIL or const2.type is ConstantType.NIL:
            jump = True
        else:
            Constant.checkSameTypes(const1, const2)
            jump = (const1.value != const2.value)

        if jump:
            Program.counter.jumpTo(jumpIndex)


class Exit(Instruction):
    def exec(self):
        symbol = self.args[0]

        exitCode = symbol.getConst()
        if exitCode.type is not ConstantType.INT:
            exitWMsg(RUN_OPERANDS_ERR, "EXIT: operand has to be int type")
        if not self._isValid(exitCode):
            exitWMsg(RUN_VAL_WORNG_ERR, "EXIT: Wrong exit code value (valid: 0 - 49)")
        
        Program.stats.insts += 1
        Program.stats.printStats()
        exit(exitCode.value)

    @staticmethod
    def _isValid(exitCode):
        """Returns bool whether exit value is valid."""
        return (exitCode.value >= 0 and exitCode.value <= 49)

class Dprint(Instruction):
    def exec(self):
        pass

class Break(Instruction):
    def exec(self):
        pass