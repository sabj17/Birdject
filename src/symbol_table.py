from src.ast import *
from src.parser import Stack


class SymbolTable:

    def __init__(self, ast_root):
        self.scope = {}
        self.scope_stack = Stack()
        self.scope_stack.push(self.scope)
        self.current_scope = self.scope_stack.top_of_stack()
        self.process_node(ast_root)

    def process_node(self, node):
        if isinstance(node, BlockNode):
            self.open_scope(node)

        elif isinstance(node, AssignNode):
            node_vars = vars(node)
            for child in node_vars.values():
                if isinstance(child, TermNode):
                    self.add_symbol(child.__str__())

    def process_all_children_nodes(self, node):
        node_children = vars(node)
        for child in node_children.values():
            if isinstance(child, list):  # if node has more than one child, the child variable will be a list
                for cc in child:
                    if isinstance(cc, AbstractNode):
                        self.process_node(cc)
            if isinstance(child, AbstractNode):
                self.process_node(child)  # powerful recursjens

    def open_scope(self, block_node):
        print(vars(block_node))
        table_scope = SymbolTable(block_node)
        self.scope[table_scope] = None  # TODO: review
        self.scope_stack.push(table_scope)
        self.current_scope = self.scope_stack.top_of_stack()

    def close_scope(self):
        print("should close last opened scope")  # TODO: can maybe be done after reaching last child node in scope
        self.scope_stack.pop()
        self.set_current_scope()

    def set_current_scope(self):
        self.current_scope = self.scope_stack.top_of_stack()

    def add_symbol(self, node_name):
        self.current_scope[node_name] = None  # TODO: review

    def get_symbol(self, node_name):
        print("gets value of a currently declared symbol. If not declared, return None/null pointer")

    def is_declared_locally(self, node_name):
        return node_name in self.current_scope

    def find_terminal_node_from_node(self, node):  # TODO: make this work
        while node.has_children:
            node_vars = vars(node)
            if isinstance(node_vars.values(), list):
                print("HELLO", node_vars)

            return node_vars
