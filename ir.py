from enum import Enum, auto

class IRContext:

    def __init__(self):
        self.register_counter = 0

    def next_register(self):
        self.register_counter += 1
        return "$T%d" % self.register_counter

class CodeObject:

    def __init__(self):
        self.ir_nodes = []
        self.result = None
        self.result_type = None

    def add_op(self, ir_op):
        self.ir_nodes.append(ir_op)

    def add(self, *objects):
        # add the code for the CodeObject object passed in the arguments (children)
        for object in objects:
            self.ir_nodes.extend(object.ir_nodes)

    def set_result(self, result):
        self.result = result

    def set_result_type(self, result_type: ResultType):
        self.result_type = result_type

class ResultType(Enum):
    INT = auto()
    FLOAT = auto()
    NONE = auto()

class IRNode:

    def __init__(self, op, args, result_type: ResultType):
        self.op = op
        self.args = args
        self.result_type = result_type

class ADDI(IRNode):

    def __init__(self, op1, op2, result):
        super().__init__("ADDI", (op1, op2, result), ResultType.INT)
        self.result_type = ResultType.INT

class SUBI(IRNode):

    def __init__(self, op1, op2, result):
        super().__init__("SUBI", (op1, op2, result), ResultType.INT)
        self.result_type = ResultType.INT

class MULTI(IRNode):

    def __init__(self, op1, op2, result):
        super().__init__("MULTI", (op1, op2, result), ResultType.INT)
        self.result_type = ResultType.INT

class DIVI(IRNode):

    def __init__(self, op1, op2, result):
        super().__init__("DIVI", (op1, op2, result), ResultType.INT)
        self.result_type = ResultType.INT

class ADDF(IRNode):

    def __init__(self, op1, op2, result):
        super().__init__("ADDF", (op1, op2, result), ResultType.FLOAT)

class SUBF(IRNode):

    def __init__(self, op1, op2, result):
        super().__init__("SUBF", (op1, op2, result), ResultType.FLOAT)

class MULTF(IRNode):
    def __init__(self, op1, op2, result):
        super().__init__("MULTF", (op1, op2, result), ResultType.FLOAT)

class DIVF(IRNode):
    def __init__(self, op1, op2, result):
        super().__init__("DIVF", (op1, op2, result), ResultType.FLOAT)

class STOREI(IRNode):
    def __init__(self, op1, result):
        super().__init__("STOREI", (op1, result), ResultType.INT)

class STOREF(IRNode):
    def __init__(self, op1, result):
        super().__init__("STOREF", (op1, result), ResultType.FLOAT)

class READI(IRNode):
    def __init__(self, result):
        super().__init__("READI", (result), ResultType.INT)

class READF(IRNode):
    def __init__(self, result):
        super().__init__("READF", (result), ResultType.FLOAT)

class WRITEI(IRNode):
    def __init__(self, op1):
        super().__init__("WRITEI", (op1), ResultType.NONE)

class WRITEF(IRNode):
    def __init__(self, op1):
        super().__init__("WRITEF", (op1), ResultType.NONE)

class WRITES(IRNode):
    def __init__(self, op1):
        super().__init__("WRITES", (op1), ResultType.NONE)
