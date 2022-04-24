"""
IPPcode22 Interpret

Author: Vilém Gottwald (xgottw07)
Project: IPP 2022 - IPPcode2022 interpret
"""

from program import Program
from arg_processor import ArgumentProcessor

cla = ArgumentProcessor()
Program.load(cla.source)
Program.interpret(cla.input, cla.stats, cla.statiFile)
