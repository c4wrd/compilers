from typing import *
from ir import *

class ASTNode:

    def __init__(self):
        self.children = [] # typeof ASTNode

    def add_child(self, node):
        self.children.append(node)

    def has_children(self):
        return len(self.children) > 0

    def debug(self, level=0):
        padding = ' ' * level
        print("%s%s" % (padding, self.__class__.__name__))
        for child in self.children:
            child.debug(level+1)

    def accept(self, context: IRContext) -> CodeObject:
        raise NotImplementedError()

class Operators:
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

class LiteralType:
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"

class VarRefNode(ASTNode):

    def __init__(self, var_name: str, type: LiteralType):
        super().__init__()
        self.var_name = var_name
        self.type = type

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()
        object.result = self.var_name
        object.result_type = self.type
        return object


class ExpressionNode(ASTNode):

    def get_left(self):
        return self.children[0]

    def get_right(self):
        return self.children[1]

class AddExprNode(ExpressionNode):

    def __init__(self, operator, left: ExpressionNode, right: ExpressionNode):
        super().__init__()
        self.operator = operator
        self.children.append(left)
        self.children.append(right)

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()

        # get code for left and right children expressions
        left_object: CodeObject = self.children[0].accept(context)
        right_object: CodeObject = self.children[1].accept(context)
        # add child expressions
        object.add(left_object, right_object)
        # set result register
        object.result = context.next_register()
        if left_object.result_type == ResultType.INT:
            if self.operator == Operators.ADD:
                object.add_op(ADDI(left_object.result, right_object.result, object.result))
            else:
                object.add_op(SUBI(left_object.result, right_object.result, object.result))
            object.result_type = ResultType.INT
        else:
            if self.operator == Operators.ADD:
                object.add_op(ADDF(left_object.result, right_object.result, object.result))
            else:
                object.add_op(SUBF(left_object.result, right_object.result, object.result))
            object.result_type = ResultType.FLOAT
        return object



class MulExprNode(ExpressionNode):

    def __init__(self, operator, left: ExpressionNode, right: ExpressionNode):
        super().__init__()
        self.operator = operator
        self.children.append(left)
        self.children.append(right)

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()

        # get code for left and right children expressions
        left_object: CodeObject = self.children[0].accept(context)
        right_object: CodeObject = self.children[1].accept(context)
        # add child expressions
        object.add(left_object, right_object)
        # set result register
        object.result = context.next_register()
        if left_object.result_type == ResultType.INT:
            if self.operator == Operators.MUL:
                object.add_op(MULTI(left_object.result, right_object.result, object.result))
            else:
                object.add_op(DIVI(left_object.result, right_object.result, object.result))
            object.result_type = ResultType.INT
        else:
            if self.operator == Operators.MUL:
                object.add_op(MULTF(left_object.result, right_object.result, object.result))
            else:
                object.add_op(DIVF(left_object.result, right_object.result, object.result))
            object.result_type = ResultType.FLOAT
        return object

class LiteralNode(ExpressionNode):
    """
    Class representing literal values
    """

    def __init__(self, value, type):
        super().__init__()
        self.value = value
        self.type = type

    def is_string(self):
        return self.type == LiteralType.STRING

    def is_int(self):
        return self.type == LiteralType.INTEGER

    def is_float(self):
        return self.type == LiteralType.FLOAT

    def as_string(self):
        return self.value

    def as_int(self):
        return int(self.value)

    def as_float(self):
        return float(self.value)

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()
        object.result = context.next_register()
        if self.is_int():
            object.result_type = ResultType.INT
            object.add_op(STOREI(self.as_int(), object.result))
        elif self.is_float():
            object.result_type = ResultType.FLOAT
            object.add_op(STOREF(self.as_float(), object.result))
        object.result = context.next_register()
        return object


class VarDeclarationNode(ASTNode):

    def __init__(self, var_ref: VarRefNode, type: str):
        super().__init__()
        self.children.append(var_ref)
        self.type = type

    def get_var(self):
        return self.children[0]

class ReadNode(ASTNode):

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()
        for node in self.children: # typeof VarRefNode
            if node.type == LiteralType.INTEGER:
                object.add_op(READI(node.var_name))
            else:
                object.add_op(READF(node.var_name))
        return object

class WriteNode(ASTNode):

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()
        for node in self.children:
            if node.type == LiteralType.INTEGER:
                object.add_op(WRITEI(node.var_name))
            elif node.type == LiteralType.FLOAT:
                object.add_op(WRITEF(node.var_name))
            else:
                object.add_op(WRITES(node.var_name))
        return object

class AssignmentNode(ASTNode):

    def __init__(self, var_ref: VarRefNode, value: ExpressionNode):
        super().__init__()
        self.var_ref = var_ref
        self.children.append(value)

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()
        left_object: CodeObject = self.children[0].accept(context)
        object.add(left_object)
        object.result = context.next_register()
        object.result_type = left_object.result_type
        if left_object.result_type == ResultType.INT:
            object.add_op(STOREI(left_object.result, object.result))
        else:
            object.add_op(STOREF(left_object.result, object.result))
        return object

class StatementListNode(ASTNode):

    def add_statement(self, statement: Union[VarDeclarationNode, AssignmentNode]):
        self.children.append(statement)

    def accept(self, context: IRContext) -> CodeObject:
        object = CodeObject()
        object.result_type = ResultType.NONE
        object.result = None
        for statement in self.children:
            object.add(statement.accept(context))
        return object

