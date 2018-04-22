from typing import List

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
