from enum import IntEnum

from ir import *


class ASTNode:

    def __init__ (self):
        self.children = []  # typeof ASTNode

    def add_child (self, node):
        self.children.append(node)

    def has_children (self):
        return len(self.children) > 0

    def debug (self, level=0):
        padding = ' ' * level
        print("%s%s" % (padding, self.__class__.__name__))
        for child in self.children:
            child.debug(level + 1)

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        raise NotImplementedError()


class Operators:
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class LiteralType:
    STRING = "string"
    INT = "integer"
    FLOAT = "float"
    NONE = "none"


class Flags(IntEnum):
    LVALUE = 1
    RVALUE = 2


class StatementListNode(ASTNode):

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()
        object.result_type = LiteralType.NONE
        object.result = None
        for statement in self.children:
            object.add(statement.accept(context, ))
        return object


class VarRefNode(ASTNode):

    def __init__ (self, var_name: str, type: LiteralType, str_value=None):
        super().__init__()
        self.var_name = var_name
        self.type = type
        self.str_value = str_value

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()
        object.result = self.var_name
        object.result_type = self.type
        return object


class ExpressionNode(ASTNode):

    def __init__ (self, flags):
        super().__init__()
        self.flags = flags

    def get_left (self):
        return self.children[0]

    def get_right (self):
        return self.children[1]


class ConditionExprNode(ASTNode):

    def __init__ (self, compop: str, left: ExpressionNode, right: ExpressionNode):
        super().__init__()
        self.lhs = left
        self.rhs = right
        self.compop = compop

    def accept(self, context: IdProviderContext, **kwargs):
        jump_label = kwargs.pop("jump_label")

        lhs = self.lhs.accept(context)
        rhs = self.rhs.accept(context)

        # we may want to jump if a condition is not met, optionally provided
        # by the parent AST node
        if "negate" in kwargs and kwargs.get("negate") == True:
            return get_negated_comp_node(self.compop, lhs.result, rhs.result, jump_label)
        else:
            return get_comp_node(self.compop, lhs.result, rhs.result, jump_label)


class IfExprNode(ASTNode):

    def __init__ (self,
                  condition: ConditionExprNode,
                  then_stmts: StatementListNode,
                  else_stmts: StatementListNode):
        super().__init__()
        self.condition = condition
        self.children.append(then_stmts)
        if else_stmts is not None:
            self.children.append(else_stmts)
            self.has_else = True
        else:
            self.has_else = False

    @property
    def then_statements(self):
        return self.children[0]

    @property
    def else_stmts(self):
        return self.children[1]

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()

        out_label = context.next_exit_label()
        then_ir = self.then_statements.accept(context)

        # we will generate different IR depending on whether
        # or not we have an else statement for efficiency
        if self.has_else:
            else_label = context.next_else_label()
            # jump to the else statement if the condition is not met
            object.add(self.condition.accept(context, jump_label=else_label, negate=True))
            object.add(then_ir) # then statements
            object.add(JUMP(out_label)) # jump to out label after then statements
            object.add(LABEL(else_label))   # label for else part
            object.add(self.else_stmts.accept(context))
            object.add(LABEL(out_label))
        else:
            object.add(self.condition.accept(context, jump_label=out_label, negate=True))
            object.add(then_ir)
            object.add(LABEL(out_label))

        return object



class WhileStmtNode(ASTNode):

    def __init__ (self, condition: ConditionExprNode, statements: StatementListNode):
        super().__init__()
        self.condition = condition
        self.children.append(statements)

    def accept (self, context: IdProviderContext, **kwargs):
        object = CodeObject()

        loop_start_label = context.next_loop_label()
        exit_label = context.next_exit_label()
        # provide the out label so the condition can jump to the correct label
        condition_ir = self.children[0].accept(context, jump_label=exit_label)  # type: CodeObject

        # provide the
        while_body_ir = self.children[1].accept(context)  # type: CodeObject

        object.add_op(LABEL(loop_start_label))  # entrypoint of loop
        object.add(condition_ir)  # comparison
        object.add(while_body_ir)  # while body
        object.add(JUMP(loop_start_label))  # jump to beginning of loop
        object.add(LABEL(exit_label))  # exit label if condition not met


class AddExprNode(ExpressionNode):

    def __init__ (self, operator, left: ExpressionNode, right: ExpressionNode):
        super().__init__(Flags.RVALUE)
        self.operator = operator
        self.children.append(left)
        self.children.append(right)

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()

        # get code for left and right children expressions
        left_object = self.children[0].accept(context, )  # type: CodeObject
        right_object = self.children[1].accept(context, )  # type: CodeObject
        # add child expressions
        object.add(left_object, right_object)
        # set result register
        object.result = context.next_temp()
        if left_object.result_type == LiteralType.INT:
            if self.operator == Operators.ADD:
                object.add_op(ADDI(left_object.result, right_object.result, object.result))
            else:
                object.add_op(SUBI(left_object.result, right_object.result, object.result))
            object.result_type = LiteralType.INT
        else:
            if self.operator == Operators.ADD:
                object.add_op(ADDF(left_object.result, right_object.result, object.result))
            else:
                object.add_op(SUBF(left_object.result, right_object.result, object.result))
            object.result_type = LiteralType.FLOAT
        return object


class MulExprNode(ExpressionNode):

    def __init__ (self, operator, left: ExpressionNode, right: ExpressionNode):
        super().__init__(Flags.RVALUE)
        self.operator = operator
        self.children.append(left)
        self.children.append(right)

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()

        # get code for left and right children expressions
        left_object = self.children[0].accept(context, )  # type: CodeObject
        right_object = self.children[1].accept(context, )  # type: CodeObject
        # add child expressions
        object.add(left_object, right_object)
        # set result register
        object.result = context.next_temp()
        if left_object.result_type == LiteralType.INT:
            if self.operator == Operators.MUL:
                object.add_op(MULTI(left_object.result, right_object.result, object.result))
            else:
                object.add_op(DIVI(left_object.result, right_object.result, object.result))
            object.result_type = LiteralType.INT
        else:
            if self.operator == Operators.MUL:
                object.add_op(MULTF(left_object.result, right_object.result, object.result))
            else:
                object.add_op(DIVF(left_object.result, right_object.result, object.result))
            object.result_type = LiteralType.FLOAT
        return object


class LiteralNode(ExpressionNode):
    """
    Class representing literal values
    """

    def __init__ (self, value, type):
        super().__init__(Flags.LVALUE)
        self.value = value
        self.type = type

    def is_string (self):
        return self.type == LiteralType.STRING

    def is_int (self):
        return self.type == LiteralType.INT

    def is_float (self):
        return self.type == LiteralType.FLOAT

    def as_string (self):
        return self.value

    def as_int (self):
        return int(self.value)

    def as_float (self):
        return float(self.value)

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()
        object.result = context.next_temp()
        if self.is_int():
            object.result_type = LiteralType.INT
            object.add_op(STOREI(self.as_int(), object.result))
        elif self.is_float():
            object.result_type = LiteralType.FLOAT
            object.add_op(STOREF(self.as_float(), object.result))
        return object


class VarDeclarationNode(ASTNode):

    def __init__ (self, var_ref: VarRefNode, type: str):
        super().__init__()
        self.children.append(var_ref)
        self.type = type

    def get_var (self):
        return self.children[0]


class ReadNode(ASTNode):

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()
        for node in self.children:  # typeof VarRefNode
            if node.type == LiteralType.INT:
                object.add_op(READI(node.var_name))
            else:
                object.add_op(READF(node.var_name))
        return object


class WriteNode(ASTNode):

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()
        for node in self.children:
            if node.type == LiteralType.INT:
                object.add_op(WRITEI(node.var_name))
            elif node.type == LiteralType.FLOAT:
                object.add_op(WRITEF(node.var_name))
            else:
                object.add_op(WRITES(node.var_name))
        return object


class AssignmentNode(ASTNode):

    def __init__ (self, var_ref: VarRefNode, value: ExpressionNode):
        super().__init__()
        self.var_ref = var_ref
        self.children.append(value)

    def accept (self, context: IdProviderContext, **kwargs) -> CodeObject:
        object = CodeObject()
        left_object = self.children[0].accept(context, )  # type: CodeObject
        object.add(left_object)
        object.result = self.var_ref.var_name
        if self.var_ref.type == LiteralType.INT:
            object.result_type = LiteralType.INT
        else:
            object.result_type = LiteralType.FLOAT
        if left_object.result_type == LiteralType.INT:
            object.add_op(STOREI(left_object.result, object.result))
        else:
            object.add_op(STOREF(left_object.result, object.result))
        return object
