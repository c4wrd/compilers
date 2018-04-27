import os, sys
from tempfile import NamedTemporaryFile
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from LittleVisitorImpl import LittleVisitorImpl, LiteralType
from asm import AsmConverter
from ir import CodeObject, IdProviderContext
from ir_builder import IRBuilder
from optimizer import IROptimizer

class CustomErrorListener(ErrorListener):

    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append("line " + str(line) + ":" + str(column) + " " + msg)

    def has_errors(self):
        return len(self.errors) > 0

def run_tiny(code):
    import subprocess

    with NamedTemporaryFile(mode="w") as file:
        for op in code:
            file.write(op.value + os.linesep)

        file.flush()

        dirname = os.path.dirname(os.path.realpath(__file__))
        cmd = ["{}/tinyvm/tiny".format(dirname), file.name]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=sys.stdin)
        while p.poll() is None:
            l = p.stdout.readline().decode()
            print(l)

        print(p.stdout.read().decode())


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

    # get parsing tree
    tree = parser.program()
    visitor = LittleVisitorImpl()

    # create AST
    prog = visitor.visitProgram(tree)

    # list of defined variables found within the program
    var_refs = visitor.var_refs

    # create IR from program
    context = IdProviderContext()
    ir = IRBuilder(prog, context)
    code = ir.get_code() # type: CodeObject

    # perform any IR optimizations
    initial_len = len(code.ir_nodes)
    optimizer = IROptimizer(code.ir_nodes)
    optimized_ir_code = optimizer.eval()
    for node in optimized_ir_code:
        node.debug()
    final_len = len(optimized_ir_code)
    # print("Optimization optimized by %.2f%%" % ((initial_len - final_len) / initial_len * 100))

    # final compilation step to convert IR -> assembly
    # converter = AsmConverter(optimized_ir_code, var_refs.values(), context)
    # code = converter.convert(debug=True, inline=False)
    # run_tiny(code)