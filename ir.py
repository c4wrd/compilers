from enum import Enum

class TemporaryContext:

    def __init__(self):
        self.count = 0
        self.label_count = 0

    def next_temp(self):
        self.count += 1
        return "$T%d" % self.count

    def next_reg(self):
       self.count += 1
       return "r%d" % self.count

    def next_exit(self):
        self.label_count += 1
        return "EXIT_%d" % self.label_count

    def next_else(self):
        self.label_count += 1
        return "ELSE_%d" % self.label_count

    def next_loop(self):
        self.label_count += 1
        return "LOOP_%d" % self.label_count

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

    def set_result_type(self, result_type):
        self.result_type = result_type

    def debug(self):
        for node in self.ir_nodes:
            node.debug()

class ResultType(Enum):
    INT = 1
    FLOAT = 2
    NONE = 4

class Ops:
    ADDI = "ADDI"
    SUBI = "SUBI"
    MULTI = "MULTI"
    DIVI = "DIVI"
    ADDF = "ADDF"
    SUBF = "SUBF"
    MULTF = "MULTF"
    DIVF = "DIVF"
    STOREI = "STOREI"
    STOREF = "STOREF"
    READI = "READI"
    READF = "READF"
    WRITEI = "WRITEI"
    WRITEF = "WRITEF"
    WRITES = "WRITES"

class IRNode:

    def __init__(self, op, args, result_type: ResultType):
        self.op = op
        self.args = args
        self.result_type = result_type

    def __str__(self):
        args = ', '.join([str(arg) for arg in self.args])
        return "%s %s \t %s" % (self.op, args, self.result_type)

    def debug(self):
        print(str(self))

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
        super().__init__("READI", (result,), ResultType.INT)

class READF(IRNode):
    def __init__(self, result):
        super().__init__("READF", (result,), ResultType.FLOAT)

class WRITEI(IRNode):
    def __init__(self, op1):
        super().__init__("WRITEI", (op1,), ResultType.NONE)

class WRITEF(IRNode):
    def __init__(self, op1):
        super().__init__("WRITEF", (op1,), ResultType.NONE)

class WRITES(IRNode):
    def __init__(self, op1):
        super().__init__("WRITES", (op1,), ResultType.NONE)

class LABEL(IRNode):
    def __init__(self, label):
        super().__init__("LABEL", (label,), ResultType.NONE)

class JUMP(IRNode):
    def __init__(self, label):
        super().__init__("JUMP", (label,), ResultType.NONE)

class GT(IRNode):
    def __init__(self, op1, op2, label):
        super().__init__("GT", (op1, op2, label), ResultType.NONE)

class GE(IRNode):
    def __init__ (self, op1, op2, label):
        super().__init__("GE", (op1, op2, label), ResultType.NONE)

class LT(IRNode):
    def __init__ (self, op1, op2, label):
        super().__init__("LT", (op1, op2, label), ResultType.NONE)

class LE(IRNode):
    def __init__ (self, op1, op2, label):
        super().__init__("LE", (op1, op2, label), ResultType.NONE)

class NE(IRNode):
    def __init__ (self, op1, op2, label):
        super().__init__("NE", (op1, op2, label), ResultType.NONE)

class EQ(IRNode):
    def __init__(self, op1, op2, label):
        super().__init__("EQ", (op1, op2, label), ResultType.NONE)

def get_comp_node(compop: str, op1, op2, label) -> IRNode:
    if str == ">":
        return GT(op1, op2, label)
    elif str == ">=":
        return GE(op1, op2, label)
    elif str == "<":
        return LT(op1, op2, label)
    elif str == "<=":
        return LE(op1, op2, label)
    elif str == "!=":
        return NE(op1, op2, label)
    elif str == "==":
        return EQ(op1, op2, label)