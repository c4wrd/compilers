from typing import List

from ast import VarRefNode, LiteralType
from ir import *

class AsmOp:
    pass

def ir(cls: object):
    cls.__class__.__name__.__hash__()


def convert_ADDI(value: ADDI) -> List[AsmOp]:
	pass


def convert_SUBI(value: SUBI) -> List[AsmOp]:
	pass


def convert_MULTI(value: MULTI) -> List[AsmOp]:
	pass


def convert_DIVI(value: DIVI) -> List[AsmOp]:
	pass


def convert_ADDF(value: ADDF) -> List[AsmOp]:
	pass


def convert_SUBF(value: SUBF) -> List[AsmOp]:
	pass


def convert_MULTF(value: MULTF) -> List[AsmOp]:
	pass


def convert_DIVF(value: DIVF) -> List[AsmOp]:
	pass


def convert_STOREI(value: STOREI) -> List[AsmOp]:
	pass


def convert_STOREF(value: STOREF) -> List[AsmOp]:
	pass


def convert_READI(value: READI) -> List[AsmOp]:
	pass


def convert_READF(value: READF) -> List[AsmOp]:
	pass


def convert_WRITEI(value: WRITEI) -> List[AsmOp]:
	pass


def convert_WRITEF(value: WRITEF) -> List[AsmOp]:
	pass


def convert_WRITES(value: WRITES) -> List[AsmOp]:
	pass

CONVERSIONS = {
    Ops.ADDI:
}

class ASMConverter:

    def __init__(self, code: List[IRNode], variables: List[VarRefNode]):
        self.ir_code = code
        self.variables = variables

    def get_string_variables(self) -> List[str]:
        # TODO need to determine if string value is stored
        return [var.var_name for var in self.variables if var.type == LiteralType.STRING]

    def get_number_variables(self) -> List[str]:
        return [var.var_name for var in self.variables if var.type == LiteralType.STRING]

    def get_variable_declarations(self) -> List[AsmOp]:
        """
        :return: List of variable declaration assembly operations
        """
        pass

    def transform(self, op: IRNode) -> List[AsmOp]:
        pass

    def convert(self) -> List[AsmOp]:
        pass