from src.ast import *
from src.ast import AST
from src.parser import Stack


class SymbolTable:

    def __init__(self):
        self.scope = {}
        self.scope_stack = Stack()
        self.scope_stack.push(self.scope)
        self.current_scope = self.scope_stack.top_of_stack()

    def open_scope(self, visitor, node):
        print("Global scope:", self.current_scope)
        node.visit_children(visitor)
        table_scope = visitor.symtab
        print("____INNER SCOPE____:", table_scope)
        self.scope[table_scope] = None  # TODO: review how it's saved / represented
        self.scope_stack.push(table_scope)

    def close_scope(self):
        self.scope_stack.pop()
        self.set_current_scope()

    def set_current_scope(self):    # TODO: Check if actually changes current scope
        #old_scope = self.current_scope
        self.current_scope = self.scope_stack.top_of_stack()
        #print('SCOPE CHANGED FROM:', old_scope, 'TO:', self.current_scope)

    def add_symbol(self, node_name):
        if node_name not in self.current_scope.keys():
            self.current_scope[node_name] = None  # TODO: add types
            #print("Node added:", self.current_scope)

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


class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class AstNodeVisitor(NodeVisitor):    # TODO: make sure only dcls are added to symbol table
    def __init__(self):
        self.symtab = SymbolTable()

    def visit_BlockNode(self, node):
        self.symtab.open_scope(self, node)
        self.symtab.close_scope()

    def visit_ClassBodyNode(self, node):
        self.symtab.open_scope(self, node)
        self.symtab.close_scope()

    def visit_AssignNode(self, node):
        self.symtab.add_symbol(node.id.name)
        node.visit_children(self)

    def visit_ClassNode(self, node):
        self.symtab.add_symbol(node.id.name)
        node.visit_children(self)

    def visit_FunctionNode(self, node):
        self.symtab.add_symbol(node.id.name)

    def visit_DotNode(self, node):
        self.symtab.get_symbol(node.ids[0].name)
