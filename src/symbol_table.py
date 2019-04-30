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
            if not self.is_declared_locally(node):
                self.add_symbol(node.__str__)

        elif isinstance(node, BlockNode):
            self.open_scope(node)

        elif isinstance(node, AssignNode):
            node_vars = vars(node)
            for child in node_vars.values():
                if isinstance(child, str):
                    self.add_symbol(child.__str__())

        self.process_all_children_nodes(node)

        if isinstance(node, BlockNode):
            self.close_scope()

    def process_all_children_nodes(self, node):
        try:
            node_children = vars(node)
            if node_children.values():
                for child in node_children.values():
                    if isinstance(child, list):  # if node has more than one child, child is a list
                        for cc in child:
                            self.process_node(cc)
                    elif isinstance(child, str):
                        self.add_symbol(child)
                    else:
                        self.process_node(child)  # powerful recursjens
        except:
            print("EXCEPTION", type(node))

    def open_scope(self, block_node):
        table_scope = SymbolTable(block_node)
        self.scope[table_scope] = None  # TODO: review
        self.scope_stack.push(table_scope)
        print(self.current_scope)
        self.set_current_scope()
        print(self.current_scope)

    def close_scope(self):
        self.scope_stack.pop()
        self.set_current_scope()

    def set_current_scope(self):
        self.current_scope = self.scope_stack.top_of_stack()

    def add_symbol(self, node_name):
        if node_name not in self.current_scope.keys():
            self.current_scope[node_name] = None  # TODO: review

    def get_symbol(self, node_name):
        if self.is_declared_locally(node_name):
            return self.current_scope[node_name]
        elif node_name in self.scope_stack.bottom_of_stack():
            global_scope = self.scope_stack.bottom_of_stack()
            return global_scope[node_name]
        else:
            raise Exception('Symbol not defined in local or global scope')

    def is_declared_locally(self, node_name):
        return node_name in self.current_scope
