import os, sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from LittleVisitorImpl import LittleVisitorImpl
from ir import CodeObject
from ir_builder import IRBuilder
from optimizer import IROptimizer


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
    code: CodeObject = ir.get_code()

    initial_len = len(code.ir_nodes)
    optimizer = IROptimizer(code.ir_nodes)
    opt_code = optimizer.eval()
    for node in opt_code:
        node.debug()
    final_len = len(opt_code)
    print("Optimization optimized by %.2f%%" % ((initial_len - final_len) / initial_len * 100))
    # walker = ParseTreeWalker()
    # listener = LittleListenerImpl()
    # walker.walk(listener, tree)