"""
Module containing generic stack class.
    
Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""

from ret_codes import *

class Stack:
    """Stack data type"""
    def __init__(self):
        """Initializes new empty stack."""
        self.stack = list()

    def push(self, value):
        """Adds value on top of stack."""
        self.stack.append(value)

    def pop(self):
        """Removes value from the top of stack and returns it.
        Pop on empty stack results in exit with value missing error.
        """
        if self.isEmpty():
            exitWMsg(RUN_VAL_MISSING_ERR, "Missing stack value" )
        return self.stack.pop()

    def isEmpty(self):
        """Returns True if stack is empty (has no elements), False otherwise"""
        return not self.stack
    
    def top(self):
        """Retruns element on top of stack"""
        return self.stack[-1]
