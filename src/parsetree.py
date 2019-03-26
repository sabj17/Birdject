from src.grammar import *


class Node:

    def __init__(self, value, parent=None):
        self.children = []
        self.value = value
        self.parent = parent
        self.is_checked = False

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value.name) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return ""


class Tree:

    def __init__(self, root):
        self.root = root
        self.current_node = root
        self.is_done = False

    def add_nodes(self, nodes):
        self.current_node.children = nodes
        for node in self.current_node.children:
            node.parent = self.current_node
            if isinstance(node.value, Terminal) or isinstance(node.value, Lambda):
                node.is_checked = True
        self.find_next()

    def find_next(self):

        if self.current_node is None:
            self.is_done = True
            return

        if all([n.is_checked for n in self.current_node.children]):
            self.current_node.is_checked = True
            self.current_node = self.current_node.parent
            self.find_next()
        else:
            for child in self.current_node.children:
                if child.is_checked is False:
                    self.current_node = child
                    break

    def __str__(self):
        return self.root.__str__()

