from src.ast import *


# p. 283 in Fischer
class SymbolTable:

    global_scope = {}

    def build_symbol_table(self, ast_root):
        # TODO: make a table for symbols to be put into - list of dictionaries?
        # Scopes can be handled by having a symbol table for each scope, or having one global symbol table.
        # Having a global symbol table makes it faster to find symbols in a search, but is more complicated
        # to set up.
        self.process_node(ast_root)

    def process_node(self, node):
        if isinstance(node, BlockNode):
            self.open_scope()

        elif isinstance(node, AssignNode):
            # print("left child should be put in symbol table as declaration/redeclaration with rhs as value")
            node_vars = vars(node)
            for child in node_vars.values():
                if isinstance(child, IdNode):
                    self.global_scope[node.__str__()] = child.name  # TODO: put lhs id as key with rhs value
                else:
                    print(child)

        # call process_node on each child of current node
        class_vars = vars(node)
        for child in class_vars.values():
            if isinstance(child, list):
                for cc in child:    # if node has more than one child, the child variable will be a list
                    if isinstance(cc, AbstractNode):
                        self.process_node(cc)
            if isinstance(child, AbstractNode):
                self.process_node(child)    # powerful recursjens

    def open_scope(self):
        print("THIS ONE OPENS SCOPES")    # TODO: how do we do this - scopes in global table or new table?
        self.global_scope

    def close_scope(self):
        print("should close last opened scope")  # TODO: can maybe be done after reaching last child node in scope

    def get_symbol(self, node_name):
        print("gets value of a currently declared symbol. If not declared, return None/null pointer")

    def is_declared_locally(self, node_name):
        print("tests if a name is declared in the current, innermost scope. Return None if not")
