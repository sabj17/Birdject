from src.ast import *


# p. 283 in Fischer
class SymbolTable:

    symbol_table = {}

    def build_symbol_table(self, AST_root):
        # TODO: make a table for symbols to be put into - list of dictionaries?
        # Scopes can be handled by having a symbol table for each scope, or having one global symbol table.
        # Having a global symbol table makes it faster to find symbols in a search, but is more complicated
        # to set up.
        self.process_node(AST_root)

    def process_node(self, node):
        if isinstance(node, BlockNode):
            self.open_scope()
        elif isinstance(node, AssignNode):
            print("left child should be put in symbol table as declaration/redeclaration with rhs as value")

        # call process_node on each child of current node
        class_vars = vars(node)
        for child in class_vars.values():
            if isinstance(child, AbstractNode):
                self.process_node(child)

    def open_scope(self):
        print("THIS ONE OPENS SCOPES")

    def close_scope(self):
        print("should close last opened scope")

    def add_symbol(self, node):
        print("THIS ONE ADDS SYMBOLS TO TABLE with values")
        self.symbol_table.append(node)

    def get_symbol(self, node_name):
        print("gets value of a currently declared symbol. If not declared, return None/null pointer")

    def is_declared_locally(self, node_name):
        print("tests if a name is declared in the current, innermost scope. Return None if not")
