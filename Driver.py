import os, sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from LittleVisitorImpl import LittleVisitorImpl
from ir_builder import IRBuilder


class CustomErrorListener(ErrorListener):

    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append("line " + str(line) + ":" + str(column) + " " + msg)

    def has_errors(self):
        return len(self.errors) > 0


if __name__ == '__main__':
    # args[1] contains the address of current testcase
    testcase_filename = sys.argv[1]
    fstream = FileStream(testcase_filename)
    lexer = LittleLexer(fstream)
    token_stream = CommonTokenStream(lexer)
    parser = LittleParser(token_stream)
    parser.removeErrorListeners()

    errorListener = CustomErrorListener()
    parser.addErrorListener(errorListener)

    tree = parser.program()
    visitor = LittleVisitorImpl()
    prog = visitor.visitProgram(tree)
    ir = IRBuilder(prog)
    code = ir.get_code()
    code.debug()
    # walker = ParseTreeWalker()
    # listener = LittleListenerImpl()
    # walker.walk(listener, tree)