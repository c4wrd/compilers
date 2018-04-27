from ir import TemporaryContext
from ast import ASTNode

class IRBuilder:

    def __init__(self, program: ASTNode, context: TemporaryContext):
        self.program = program
        self.context = context

    def get_code(self):
        return self.program.accept(self.context)