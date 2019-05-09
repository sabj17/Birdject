from src.ast import *
from src.ast import AST
from src.parser import Stack


class SymbolCrapTable:

    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self.symbols = {}
        self.scope_name = scope_name    # TODO delete if it never gets used
        self.scope_level = scope_level  # TODO delete if it never gets used - might be redundant bcause enclosing scope
        self.enclosing_scope = enclosing_scope

    def new_scope(self, node, enclosing_scope):
        scope_name = type(node)     #TODO do something else for block scopes that comes out of nowhere

        scope_object = SymbolCrapTable(
            scope_name=scope_name,
            scope_level=enclosing_scope.scope_level + 1,
            enclosing_scope=enclosing_scope
        )
        return scope_object

    def add_symbol(self, node_name):
        #print('Insert: %s' % node)
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
            raise Exception('Symbol not found')




class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class AstCrapNodeVisitor(NodeVisitor):    # TODO: make sure only dcls are added to symbol table
    def __init__(self):
        self.current_scope = SymbolCrapTable(
            scope_name='global',
            scope_level=1,
            )

    def visit_BlockNode(self, node):
        #print('########### Before ', self.current_scope.symbols)
        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(node, self.current_scope)
        self.current_scope = inner_scope
        node.visit_children(self)

        #print('########### After ', self.current_scope.symbols)

        self.current_scope = enclosing_scope
        self.current_scope.symbols[inner_scope] = 'Block_Scope'


    def visit_ClassNode(self, node):
        self.current_scope.symbols[node.id.name] = object

        print('_____________ Before ', self.current_scope.symbols)
        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(node, self.current_scope)
        self.current_scope = inner_scope
        node.body_part.visit_children(self)

        print('___________ After ', self.current_scope.symbols)

        self.current_scope = enclosing_scope
        self.current_scope.symbols[str(node.id.name + 'Scope')] = inner_scope
        print('___________ After ', self.current_scope.symbols)

    def visit_AssignNode(self, node):
        print(node.expression)
        if isinstance(node.expression, BoolNode):
            self.current_scope.symbols[node.id.name] = bool # TODO maybe just bool? But that's a native type
        elif isinstance(node.expression, NewObjectNode):
            self.current_scope.symbols[node.id.name] = node.expression.id.name
        elif isinstance(node.expression, IntegerNode):
            self.current_scope.symbols[node.id.name] = int
        elif isinstance(node.expression, FloatNode):
            self.current_scope.symbols[node.id.name] = float
        elif isinstance(node.expression, StringNode):
            self.current_scope.symbols[node.id.name] = str
        elif isinstance(node.expression, BinaryExpNode):
            self.current_scope.symbols[node.id.name] = 'sumthing'
        elif isinstance(node.expression, IdNode):
            #self.current_scope.symbols[node.id.name] = self.current_scope.lookup(node.id.name)
            pass
        else:
            self.current_scope.symbols[node.id.name] = None

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

    def visit_RunNode(self, node):
        # finds the formal param of a dotnode
        if isinstance(node.id, DotNode):
            last_id = node.id.ids[-1].name
            var = self.current_scope
            formal_param = None
            for id in node.id.ids:
                if id.name == last_id:
                    formal_param = var.lookup(id.name)
                else:
                    var = var.lookup(str(id.name + 'Scope'))

            # TODO make with real types when we get that
            if formal_param != self.get_actual_params(node):
                raise Exception('Type error: missing paramater or mismatch in types')

        # What that should happen when the runNode dosen't have following dotNodes
        elif isinstance(node.id, IdNode):
            # TODO make with real types when we get that
            if self.current_scope.lookup(node.id.name) != self.get_actual_params(node):
                raise Exception('Type error: missing paramater or mismatch in types')

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
                    # print('idNode param name = ', param.name)
                    param_list.append('type' + str(i))
                    i += 1
            else:
                param_list.append('type1')

        return param_list

    def add_params_to_scope(self, node):
        if isinstance(node.params.id_list, list):
            for param in node.params.id_list:
                self.current_scope.add_symbol(param.name)
        else:
            self.current_scope.add_symbol(node.params.id_list.name)