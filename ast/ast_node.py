from typing import List

class ASTNode:

    def __init__(self):
        self.children = [] # typeof ASTNode

    def add_child(self, node):
        self.children.append(node)

    def has_children(self):
        return len(self.children) > 0