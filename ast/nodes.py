from ast.ast_node import ASTNode
from typing import *

class Operators:
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

class LiteralTypes:
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"

class VarRefNode(ASTNode):

    def __init__(self, var_name: str, type: str):
        super().__init__()
        self.var_name = var_name
        self.type = type

    def is_int(self):
        return self.type == "int"

    def is_float(self):
        return self.type == "float"

class ExpressionNode(ASTNode):

    def get_left(self):
        return self.children[0]

    def get_right(self):
        return self.children[1]

class AddExpr(ExpressionNode):

    def __init__(self, operator, left: ExpressionNode, right: ExpressionNode):
        super().__init__()
        self.operator = operator
        self.children.append(left)
        self.children.append(right)

class MulExpr(ExpressionNode):

    def __init__(self, operator):
        super().__init__()
        self.operator = operator

class LiteralNode(ExpressionNode):
    """
    Class representing literal values
    """

    def __init__(self, value, type):
        super().__init__()
        self.value = value
        self.type = type

    def is_string(self):
        return self.type == LiteralTypes.STRING

    def is_int(self):
        return self.type == LiteralTypes.INTEGER

    def is_float(self):
        return self.type == LiteralTypes.FLOAT

    def as_string(self):
        return self.value

    def as_int(self):
        return int(self.value)

    def as_float(self):
        return float(self.value)

class VarDeclarationNode(ASTNode):

    def __init__(self, var_name: str, value: ExpressionNode):
        super().__init__()
        self.var_name = var_name
        self.children.append(value)

    def get_expr(self):
        return self.children[0]

class AssignmentNode(ASTNode):

    def __init__(self, var_name, value: ExpressionNode):
        super().__init__()
        self.var_name = var_name
        self.children.append(value)


class StatementListNode(ASTNode):

    def add_statement(self, statement: Union[VarDeclarationNode, AssignmentNode]):
        self.children.append(statement)