from src.grammar import *
from graphviz import Digraph, nohtml
import random


class Node:

    def __init__(self, symbol, value, parent=None):
        self.name = symbol.name
        self.children = []
        self.value = value
        self.symbol = symbol
        self.parent = parent
        self.is_checked = False

    def add_child(self, child):
        self.children.append(child)

    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.name + ": " + str(self.value)))
        if parent is not None:
            graph.edge(parent, id)

        for child in self.children:
            child.graph(graph, id)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.symbol.name) + "\n"
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
            if isinstance(node.symbol, Lambda):
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

    def leaf_found(self, value):
        self.current_node.value = value
        self.find_next()

    def graph(self):
        graph = Digraph('G', node_attr={'style': 'filled'}, graph_attr={'ratio': 'fill', 'ranksep': '1.5'})
        graph.attr(overlap='false')
        self.root.graph(graph)
        graph.save(filename='parse_tree.gv')

    def __str__(self):
        return self.root.__str__()


