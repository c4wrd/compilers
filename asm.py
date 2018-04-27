import re

from typing import List, Callable

from ast import VarRefNode, LiteralType
from ir import *

temp_pattern = re.compile(r"\$T(\d+)")

def get_arg_representation(value: str):
    """
    Parses an operation argument and determines if it
    is a temporary variable. If so, it will return the index
    that the temporary variable represents, and returns as
    a register
    :param value:
    :return:
    """
    # ignore integers and floating point literals
    if not isinstance(value, str):
        return value

    match = temp_pattern.match(value)
    if match is not None:
        return "r{}".format(match.group(1))
    return value

def getargs(args):
    values = [get_arg_representation(arg) for arg in args]
    # if unpacking a single argument (such as for read/write)
    # we will return the first argument for easier assignment
    if len(values) == 1:
        return values[0]
    return values

class AsmOp:
    def __init__(self, string: str, *args):
        self.value = string.format(*args)

def make(string: str, *args) -> AsmOp:
    # helper function to make assembly composition easier
    return AsmOp(string, *args)


def handler(func: Callable):
    """
    Helper function to return a callable method that will
    invoke the proper handler provided by the parameter 'func'.
    """

    def anonymous_func(value: IRNode, context):
        return func(value, context)

    return anonymous_func


def convert_ADDI(value: ADDI, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("addi {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]

def convert_SUBI(value: SUBI, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("subi {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]


def convert_MULTI(value: MULTI, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("muli {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]

def convert_DIVI(value: DIVI, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("divi {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]


def convert_ADDF(value: ADDF, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("addr {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]


def convert_SUBF(value: SUBF, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("subr {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]


def convert_MULTF(value: MULTF, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("mulr {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]


def convert_DIVF(value: DIVF, context: IdProviderContext) -> List[AsmOp]:
    op1, op2, result = getargs(value.args)
    temp_register = context.next_reg()
    return [
        make("move {} {}", op1, temp_register),
        make("divr {} {}", op2, temp_register),
        make("move {} {}", temp_register, result)
    ]


def convert_STOREI(value: STOREI, context: IdProviderContext) -> List[AsmOp]:
    op1, result = getargs(value.args)
    return [
        make("move {} {}", op1, result)
    ]


def convert_STOREF(value: STOREF, context: IdProviderContext) -> List[AsmOp]:
    op1, result = getargs(value.args)
    return [
        make("move {} {}", op1, result)
    ]


def convert_READI(value: READI, context: IdProviderContext) -> List[AsmOp]:
    result = getargs(value.args)
    return [
        make("sys readi {}", result)
    ]


def convert_READF(value: READF, context: IdProviderContext) -> List[AsmOp]:
    result = getargs(value.args)
    return [
        make("sys readr {}", result)
    ]


def convert_WRITEI(value: WRITEI, context: IdProviderContext) -> List[AsmOp]:
    op1 = getargs(value.args)
    return [
        make("sys writei {}", op1)
    ]


def convert_WRITEF(value: WRITEF, context: IdProviderContext) -> List[AsmOp]:
    op1 = getargs(value.args)
    return [
        make("sys writer {}", op1)
    ]


def convert_WRITES(value: WRITES, context: IdProviderContext) -> List[AsmOp]:
    op1 = getargs(value.args)
    return [
        make("sys writes {}", op1)
    ]

def convert_JUMP(value: JUMP, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_LABEL(value: LABEL, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_GT(value: GT, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_GE(value: GE, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_LT(value: LT, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_LE(value: LE, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_NE(value: NE, context: IdProviderContext) -> List[AsmOp]:
    pass


def convert_EQ(value: EQ, context: IdProviderContext) -> List[AsmOp]:
    pass


"""
Map of operation types to the appropriate method
that will convert the IR code into assembly
"""
CONVERSIONS = {
    Ops.ADDI: handler(convert_ADDI),
    Ops.SUBI: handler(convert_SUBI),
    Ops.MULTI: handler(convert_MULTI),
    Ops.DIVI: handler(convert_DIVI),
    Ops.ADDF: handler(convert_ADDF),
    Ops.SUBF: handler(convert_SUBF),
    Ops.MULTF: handler(convert_MULTF),
    Ops.DIVF: handler(convert_DIVF),
    Ops.STOREI: handler(convert_STOREI),
    Ops.STOREF: handler(convert_STOREF),
    Ops.READI: handler(convert_READI),
    Ops.READF: handler(convert_READF),
    Ops.WRITEI: handler(convert_WRITEI),
    Ops.WRITEF: handler(convert_WRITEF),
    Ops.WRITES: handler(convert_WRITES),
    Ops.JUMP: handler(convert_JUMP),
    Ops.LABEL: handler(convert_LABEL),
    Ops.GT: handler(convert_GT),
    Ops.GE: handler(convert_GE),
    Ops.LT: handler(convert_LT),
    Ops.LE: handler(convert_LE),
    Ops.NE: handler(convert_NE),
    Ops.EQ: handler(convert_EQ)
}


class AsmConverter:
    def __init__(self, code: List[IRNode], variables: List[VarRefNode], context: IdProviderContext):
        self.ir_ops = code
        self.variables = variables
        self.context = context

    def __get_string_variables__(self) -> List[AsmOp]:
        return [make("str {} {}", var.var_name, var.str_value)
                for var in self.variables
                if var.type == LiteralType.STRING]

    def __get_number_variables__(self) -> List[AsmOp]:
        return [make("var {}", var.var_name)
                for var in self.variables
                if var.type != LiteralType.STRING]

    def __transform__(self, op: IRNode) -> List[AsmOp]:
        # TODO handle label (?)
        return CONVERSIONS[op.op](op, self.context)

    def convert(self, debug=False, inline=True) -> List[AsmOp]:
        ops = []
        if debug and not inline:
            ops.extend([make("; {}", str(op)) for op in self.ir_ops])
        ops.extend(self.__get_string_variables__())
        ops.extend(self.__get_number_variables__())

        for op in self.ir_ops:
            # if debugging, print IR code before assembly code
            if debug and inline:
                ops.append(AsmOp("; {}", str(op)))
            ops.extend(self.__transform__(op))

        # add op code for terminating program
        ops.append(make("sys halt"))

        if debug:
            print('\n'.join(map(lambda op: op.value, ops)))

        return ops
