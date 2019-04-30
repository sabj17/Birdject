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
        if isinstance(node, TermNode):
            self.add_symbol(node.__str__)

        elif isinstance(node, BlockNode):
            self.open_scope(node)

        elif isinstance(node, AssignNode):
            node_vars = vars(node)
            for child in node_vars.values():
                if isinstance(child, TermNode):
                    self.add_symbol(child.__str__())

        self.process_all_children_nodes(node)

        if isinstance(node, BlockNode):
            self.close_scope()

    def process_all_children_nodes(self, node):
        node_children = vars(node)
        print(type(node), node_children)
        for child in node_children.values():
            if isinstance(child, list):  # if node has more than one child, the child variable will be a list
                for cc in child:
                    self.process_node(cc)
            elif isinstance(child, AbstractNode):
                self.process_node(child)  # powerful recursjens

    def open_scope(self, block_node):
        print(vars(block_node))
        table_scope = SymbolTable(block_node)
        self.scope[table_scope] = None    # TODO: review
        self.scope_stack.push(table_scope)
        self.current_scope = self.scope_stack.top_of_stack()

    def close_scope(self):
        print("should close last opened scope")  # TODO: can maybe be done after reaching last child node in scope
        self.scope_stack.pop()
        self.set_current_scope()

    def set_current_scope(self):
        self.current_scope = self.scope_stack.top_of_stack()

    def add_symbol(self, node_name):
        if node_name not in self.current_scope.keys():
            self.current_scope[node_name] = None  # TODO: review

    def get_symbol(self, node_name):
        print("gets value of a currently declared symbol. Check current scope only?")
        if self.is_declared_locally(node_name):
            return self.current_scope[node_name]
        elif node_name in self.scope_stack.bottom_of_stack():
            global_scope = self.scope_stack.bottom_of_stack()
            return global_scope[node_name]
        else:
            raise Exception('Symbol not defined in local or global scope')

    def is_declared_locally(self, node_name):
        return node_name in self.current_scope
