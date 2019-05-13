from ast import *


class SymbolCrapTable:

    def __init__(self, enclosing_scope=None):
        self.symbols = {}
        self.enclosing_scope = enclosing_scope

    def new_scope(self, enclosing_scope):
        scope_object = SymbolCrapTable(
            enclosing_scope=enclosing_scope
        )
        return scope_object

    def lookup(self, name):
        # 'symbol' is either an instance of the 'type' or None
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        else:
            raise Exception('Symbol not found', name)


class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class AstCrapNodeVisitor(NodeVisitor):
    def __init__(self):
        self.current_scope = SymbolCrapTable()

    def visit_BlockNode(self, node):
        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(self.current_scope)
        self.current_scope = inner_scope
        node.visit_children(self)

        self.current_scope = enclosing_scope
        self.current_scope.symbols[inner_scope] = 'Block_Scope'

    def visit_ClassNode(self, node):
        self.current_scope.symbols[node.id.name] = object

        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(self.current_scope)
        self.current_scope = inner_scope
        node.body_part.visit_children(self)

        self.current_scope = enclosing_scope
        self.current_scope.symbols[str(node.id.name + 'Scope')] = inner_scope

    def visit_AssignNode(self, node):

        if isinstance(node.expression, NewObjectNode):
            self.current_scope.symbols[node.id.name] = node.expression.id.name
        elif isinstance(node.expression, BinaryExpNode):
            self.current_scope.symbols[node.id.name] = self.eval_bin_expr_type(node.expression)
        elif isinstance(node.expression, IdNode):
            self.current_scope.symbols[node.id.name] = self.current_scope.lookup(node.expression.name)
        elif isinstance(node.expression, TermNode):
            self.current_scope.symbols[node.id.name] = self.eval_term_node_type(node.expression)

    def eval_term_node_type(self, term_node):
        type_of_term_node = None

        if isinstance(term_node, BoolNode):
            type_of_term_node = bool
        elif isinstance(term_node, IntegerNode):
            type_of_term_node = int
        elif isinstance(term_node, FloatNode):
            type_of_term_node = float
        elif isinstance(term_node, StringNode):
            type_of_term_node = str
        elif isinstance(term_node, IdNode):
            type_of_term_node = self.current_scope.lookup(term_node.name)

        return type_of_term_node

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

            if isinstance(expr, BinaryExpNode) or isinstance(expr, UnaryExpNode):
                self.eval_bin_expr_type(expr)

        return final_type

    def visit_FunctionNode(self, node):
        outer_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(self.current_scope)
        param_list = []

        # Gets the formal parameters with fake type(s) 1,2,3.
        if node.params is not None:
            param_list = self.get_formal_params(node)

        self.current_scope.symbols[node.id.name] = param_list
        self.current_scope = inner_scope

        if node.params is not None:     # Adds the parameters to the scope
            self.add_params_to_scope(node)

        node.block.visit_children(self)
        self.current_scope = outer_scope
        self.current_scope.symbols[str(node.id.name + 'Scope')] = inner_scope

    def visit_IfNode(self, node):
        LHS_type_of_equal = None
        RHS_type_of_equal = None

        if isinstance(node.expression, IdNode):
            if self.current_scope.lookup(node.expression.name) != bool:
                raise Exception(TypeError, node.expression.name)
        elif isinstance(node.expression, EqualsNode):
            if isinstance(node.expression.expr1, TermNode):
                LHS_type_of_equal = self.eval_term_node_type(node.expression.expr1)
            elif isinstance(node.expression.expr1, BinaryExpNode):
                LHS_type_of_equal = self.eval_bin_expr_type(node.expression.expr1)

            if isinstance(node.expression.expr2, TermNode):
                RHS_type_of_equal = self.eval_term_node_type(node.expression.expr2)
            elif isinstance(node.expression.expr2, BinaryExpNode):
                RHS_type_of_equal = self.eval_bin_expr_type(node.expression.expr2)

            if LHS_type_of_equal != RHS_type_of_equal:
                raise Exception(TypeError, LHS_type_of_equal, 'and', RHS_type_of_equal, 'is not the same')

        node.visit_children(self)

    def visit_ReturnNode(self, node):
        if isinstance(node.expression, IdNode):
            self.current_scope.lookup(node.expression.name)

    def visit_RunNode(self, node):
        # Gets the formal parameters if it's a dotNode
        if isinstance(node.id, DotNode):  # Looks for if Class.method exist
            last_id = node.id.ids[-1].name
            temp_scope = self.current_scope
            formal_param = None
            for id in node.id.ids:
                if id.name == last_id:
                    formal_param = temp_scope.lookup(id.name)
                else:
                    temp_scope = temp_scope.lookup(str(id.name + 'Scope'))

            # Compares the amount of formal and actual parameters
            if len(formal_param) != len(self.get_actual_params(node)):
                raise Exception('Type error: missing parameter or mismatch in types')

        # Get the formal parameters if the runNode just has a IdNode and not a DotNode
        # Compares the amount of formal and actual parameters
        elif isinstance(node.id, IdNode):
            if len(self.current_scope.lookup(node.id.name)) != len(self.get_actual_params(node)):
                raise Exception('Type error: missing parameter or mismatch in types')

    # Returns a list of types of the actual parameters
    def get_actual_params(self, runNode):
        param_list = []

        if runNode.params is not None:
            if isinstance(runNode.params.expr_list, list):
                for param in runNode.params.expr_list:
                    if isinstance(param, IdNode):
                        param_list.append(self.current_scope.lookup(param.name))
                    elif isinstance(param, TermNode):
                        param_list.append(self.eval_term_node_type(param))
                    elif isinstance(param, BinaryExpNode):
                        param_list.append(self.eval_bin_expr_type(param))

        return param_list

    def get_formal_params(self, funcNode):
        param_list = []
        i = 1

        if isinstance(funcNode.params.id_list, list):
            for param in funcNode.params.id_list:
                param_list.append('funcParam' + str(i))
                i += 1
        else:
            param_list.append('funcParam1')

        return param_list

    def add_params_to_scope(self, funcNode):
        if isinstance(funcNode.params.id_list, list):
            for param in funcNode.params.id_list:
                self.current_scope.symbols[param.name] = 'formalParam'
        else:
            self.current_scope.symbols[funcNode.params.id_list.name] = 'formalParam'
