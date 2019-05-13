from ast import *


class SymbolCrapTable:

    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self.symbols = {}
        self.scope_name = scope_name    # TODO delete if it never gets used
        self.scope_level = scope_level  # TODO delete if it never gets used - might be redundant because enclosing scope
        self.enclosing_scope = enclosing_scope

    def new_scope(self, node, enclosing_scope):
        scope_name = type(node)     # TODO do something else for block scopes that come out of nowhere

        scope_object = SymbolCrapTable(
            scope_name=scope_name,
            scope_level=enclosing_scope.scope_level + 1,
            enclosing_scope=enclosing_scope
        )
        return scope_object

    def add_symbol(self, node_name):
        self.symbols[node_name] = 'type'

    def lookup(self, name):
        # 'symbol' is either an instance of the 'type' or None
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        else:
            raise Exception('Symbol not found', symbol)


class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class AstCrapNodeVisitor(NodeVisitor):
    def __init__(self):
        self.current_scope = SymbolCrapTable(
            scope_name='global',
            scope_level=1,
            )

    def visit_BlockNode(self, node):
        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(node, self.current_scope)
        self.current_scope = inner_scope
        node.visit_children(self)

        self.current_scope = enclosing_scope
        self.current_scope.symbols[inner_scope] = 'Block_Scope'

    def visit_ClassNode(self, node):
        self.current_scope.symbols[node.id.name] = object

        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(node, self.current_scope)
        self.current_scope = inner_scope
        node.body_part.visit_children(self)

        self.current_scope = enclosing_scope
        self.current_scope.symbols[str(node.id.name + 'Scope')] = inner_scope

    def visit_AssignNode(self, node):
        if isinstance(node.expression, BoolNode):
            self.current_scope.symbols[node.id.name] = bool
        elif isinstance(node.expression, NewObjectNode):
            self.current_scope.symbols[node.id.name] = node.expression.id.name
        elif isinstance(node.expression, IntegerNode):
            self.current_scope.symbols[node.id.name] = int
        elif isinstance(node.expression, FloatNode):
            self.current_scope.symbols[node.id.name] = float
        elif isinstance(node.expression, StringNode):
            self.current_scope.symbols[node.id.name] = str
        elif isinstance(node.expression, BinaryExpNode):
            self.current_scope.symbols[node.id.name] = self.eval_bin_expr_type(node.expression)
        elif isinstance(node.expression, IdNode):
            self.current_scope.symbols[node.id.name] = self.current_scope.lookup(node.expression.name)
        else:
            self.current_scope.symbols[node.id.name] = None

    def eval_bin_expr_type(self, binExpNode):
        final_type = None
        id_type = None

        for expr in vars(binExpNode).values():
            if isinstance(expr, IdNode):    # Gets the type of the IdNode
                id_type = self.current_scope.lookup(expr.name)

            if isinstance(expr, StringNode) or id_type == str:
                final_type = str
            elif (final_type == int or final_type == None) and (isinstance(expr, FloatNode) or id_type == float):
                final_type = float
            elif (final_type == None) and (isinstance(expr, IntegerNode) or id_type == int):
                final_type = int

            if (not isinstance(binExpNode, PlusNode)) and (final_type == str):
                raise Exception(TypeError, expr)

            if isinstance(expr, BinaryExpNode):
                self.eval_bin_expr_type(expr)

        return final_type

    def visit_FunctionNode(self, node):
        outer_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(node, self.current_scope)
        param_list = []

        ####################### Test until we get real types ####################################
        if node.params is not None:
            param_list = self.get_formal_params(node)

        self.current_scope.symbols[node.id.name] = param_list
        #########################################################################################
        self.current_scope = inner_scope

        if node.params is not None:
            self.add_params_to_scope(node)

        node.block.visit_children(self)
        self.current_scope = outer_scope
        self.current_scope.symbols[str(node.id.name + 'Scope')] = inner_scope

    def visit_IfNode(self, node):
        if isinstance(node.expression, IdNode):
            if self.current_scope.lookup(node.expression.name) != bool:
                raise Exception(TypeError, node.expression.name)

    def visit_RunNode(self, node):
        if isinstance(node.id, DotNode):  # Looks for if Class.method exist
            last_id = node.id.ids[-1].name
            temp_scope = self.current_scope
            formal_param = None
            for id in node.id.ids:
                if id.name == last_id:
                    formal_param = temp_scope.lookup(id.name)
                else:
                    temp_scope = temp_scope.lookup(str(id.name + 'Scope'))

            # TODO make with real types when we get that
            print("LEN:", len(formal_param), len(self.get_actual_params(node)))
            if len(formal_param) != len(self.get_actual_params(node)):
                raise Exception('Type error: missing parameter or mismatch in types')

        # What that should happen when the runNode dosen't have following dotNodes
        elif isinstance(node.id, IdNode):
            # TODO make with real types when we get that
            print("LEN:", len(self.current_scope.lookup(node.id.name)), len(self.get_actual_params(node)))
            if len(self.current_scope.lookup(node.id.name)) != len(self.get_actual_params(node)):
                raise Exception('Type error: missing parameter or mismatch in types')

    def get_formal_params(self, node):
        param_list = []
        i = 1

        if isinstance(node.params.id_list, list):
            for param in node.params.id_list:
                param_list.append('type' + str(i))
                i += 1
        else:
            param_list.append('type1')

        return param_list

    def get_actual_params(self, node):
        param_list = []
        i = 1
        if node.params is not None:
            if isinstance(node.params.expr_list, list):
                for param in node.params.expr_list:
                    param_list.append('type' + str(i))
                    i += 1
            else:
                param_list.append('type1')

        return param_list

    def add_params_to_scope(self, node):
        if isinstance(node.params.id_list, list):
            for param in node.params.id_list:
                self.current_scope.add_symbol(param.name)
                print("ADDING", param.name)
        else:
            self.current_scope.add_symbol(node.params.id_list.name)
