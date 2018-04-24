from ir import *
from typing import List

class IROptimizer:

    def __init__(self, nodes: List[IRNode]):
        self.nodes = nodes
        self.optimizations = [RedundantStore()]

    def eval(self) -> List[IRNode]:
        for opt in self.optimizations:
            self.nodes = opt.eval(self.nodes)
        return self.nodes

class IRPattern:

    def __init__(self, window_size):
        self.window_size = window_size

    def can_evaluate(self, ir_nodes: List[IRNode], start, end):
        # ensure we can operate on these nodes
        return end - start == self.window_size and end < len(ir_nodes)

    def stich(self, ir_nodes: List[IRNode], start, end, new_ir_nodes: List[IRNode]) -> List[IRNode]:
        """
        Stiches in the new ir nodes in the ir_nodes list, replacing the nodes found in
        start->end
        """
        return_nodes = ir_nodes[0:start]
        return_nodes.extend(new_ir_nodes)
        return_nodes.extend(ir_nodes[end:])
        return return_nodes

    def eval(self, ir_nodes: List[IRNode]):
        for i in range(len(ir_nodes)):
            start = i
            end = i + self.window_size
            if self.can_evaluate(ir_nodes, i, i+self.window_size):
                ir_nodes = self.__eval__(ir_nodes, start, end)
        return ir_nodes

    def __eval__(self, ir_nodes: List[IRNode], start, end) -> List[IRNode]:
        raise NotImplementedError()

class RedundantStore(IRPattern):
    """
    Fixes any places where we have an r-value stored in a temporary register
    that is immediately stored in a variable
    """

    def __init__(self):
        super().__init__(2)

    def __eval__ (self, ir_nodes: List[IRNode], start, end) -> List[IRNode]:
        nodes = ir_nodes[start:end]
        if nodes[0].op == Ops.STOREI and nodes[1].op == Ops.STOREI \
                and nodes[0].args[1] == nodes[1].args[0]:
            return self.stich(ir_nodes, start, end, [STOREI(nodes[0].args[0], nodes[1].args[1])])
        return ir_nodes


