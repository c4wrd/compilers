from ir import IRContext
from ast import ASTNode

class IRBuilder:

    def __init__(self, program: ASTNode):
        self.program = program
        self.context = IRContext()

    def get_code(self):
        return self.program.accept(self.context)