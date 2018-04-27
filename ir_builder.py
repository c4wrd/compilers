from ir import RegisterContext
from ast import ASTNode

class IRBuilder:

    def __init__(self, program: ASTNode, context: RegisterContext):
        self.program = program
        self.context = context

    def get_code(self):
        return self.program.accept(self.context)