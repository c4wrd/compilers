import os, sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from io import StringIO

class MyErrorListener(ErrorListener):

    def __init__(self):
        self.output = StringIO()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write("line " + str(line) + ":" + str(column) + " " + msg)

    def print(self):
        print(self.output.getvalue())


if __name__ == '__main__':
    # args[1] contains the address of current testcase
    testcase_filename = sys.argv[1]
    fstream = FileStream(testcase_filename)
    lexer = LittleLexer(fstream)
    token_stream = CommonTokenStream(lexer)
    parser = LittleParser(token_stream)
    parser.removeErrorListeners()
    listener = MyErrorListener()
    parser.addErrorListener(listener)

    program = parser.program()
    if program.exception is not None:
        print("Not accepted")
        listener.print()
    else:
        print("Accepted")