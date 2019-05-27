from src.ast import *


class SymbolTable:

    def __init__(self, enclosing_scope=None):
        self.symbols = {}
        self.enclosing_scope = enclosing_scope
        self.blockscope_counter = 1
        self.predefined_types = ['Light', 'Switch', 'Thermometer', 'Window', 'Radiator', 'List']
        self.predef_func_not_on_objects = ['print', 'wait']
        self.predefined_functions = {'isTurnedOn': [],  # no input parameters
                                     'setMode': [bool], # one bool as input parameter
                                     'getTemp': [],     # no input parameters
                                     'changeMode': [],  # no input parameters
                                     'close' : [],      # no input parameters
                                     'openTo' : [int], # int as input parameter
                                     'increase' : [],   # no input parameters
                                     'decrease' : [], # no input parameters
                                     'setHeatLevel' : [int], # int as input parameter
                                     'getHeatLevel' : []} # no input parameters

    def new_scope(self, enclosing_scope):
        scope_object = SymbolTable(
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
            raise NameError(name, 'was not found in the symbol table.')

    def get_outer_scope_of_symbol(self, name):
        if self.symbols.get(name) is None:
            return self.enclosing_scope.get_outer_scope_of_symbol(name)
        else:
            return self


class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class BuildSymbolTableVisitor(NodeVisitor):
    def __init__(self):
        self.current_scope = SymbolTable()

    def visit_BlockNode(self, node):
        enclosing_scope = self.current_scope
        inner_scope = self.current_scope.new_scope(self.current_scope)
        self.current_scope = inner_scope
        node.visit_children(self)

        self.current_scope = enclosing_scope
        self.current_scope.symbols['Block_scope'+str(self.current_scope.blockscope_counter)] = inner_scope
        self.current_scope.blockscope_counter += 1

    def visit_ClassNode(self, node):
        self.current_scope.symbols[node.id.name] = 'classType'

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
        elif isinstance(node.expression, UnaryExpNode):
            self.current_scope.symbols[node.id.name] = self.ignore_unary_symbols(node.expression.expression)
        elif isinstance(node.expression, RunNode):
            self.current_scope.symbols[node.id.name] = self.get_returnType_from_func(node.expression)

    def ignore_unary_symbols(self, unaryNode):
        if isinstance(unaryNode, UnaryExpNode):
            return self.ignore_unary_symbols(unaryNode.expression)
        elif isinstance(unaryNode, BinaryExpNode):
            return self.eval_bin_expr_type(unaryNode)
        elif isinstance(unaryNode, RunNode):
            return self.get_returnType_from_func(unaryNode)
        else:
            return self.eval_term_node_type(unaryNode)


    def get_returnType_from_func(self, runNode):
        self.visit_RunNode(runNode) # Populate the node before it can get the return type

        if isinstance(runNode.id, DotNode):
            return_type = self.get_returnType_dotnode(runNode)
        else:
            return_type = self.get_returnType_not_dotnode(runNode)

        return return_type

    def get_returnType_not_dotnode(self, runNode):
        func_scope = self.current_scope.lookup(str(runNode.id.name + 'Scope'))
        return_type = func_scope.lookup('returnType')
        return return_type

    def get_returnType_dotnode(self, runNode):
        return_types_of_predef_functions = {'isTurnedOn' : bool,
                                            'setMode' : bool,
                                            'getTemp' : float,
                                            'changeMode' : bool,
                                            'close' : int,
                                            'openTo' : int,
                                            'increase' : int,
                                            'decrease' : int,
                                            'setHeatLevel' : 'void',
                                            'getHeatLevel' : int,
                                            }
        last_id = runNode.id.ids[-1].name  # Is the last name of a dot sequence like LivingRoom.light.setState
        temp_scope = self.current_scope
        return_type = None

        for id in runNode.id.ids:
            # Checks if the last id in the dot sequence is a built in function
            if self.current_scope.predefined_functions.get(last_id) is not None:
                return_type = return_types_of_predef_functions.get(last_id)

            # Gets the parameters of the function which matches the last id instead of entering it's scope
            elif id.name == last_id:
                temp_scope = temp_scope.lookup(id.name + 'Scope')
                return_type = temp_scope.lookup('returnType')
            else:
                temp_scope = temp_scope.lookup(str(id.name + 'Scope'))

        return return_type

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
        left_child = self.eval_type_of_child(binExpNode.expr1)
        right_child = self.eval_type_of_child(binExpNode.expr2)

        self.check_binExpr_exceptions(binExpNode, left_child, right_child)
        final_type = self.type_w_higest_precedence(right_child, left_child)
        return final_type

    def eval_type_of_child(self, child):
        child_type = None
        if isinstance(child, TermNode):
            child_type = self.eval_term_node_type(child)
        elif isinstance(child, UnaryExpNode):
            child_type = self.ignore_unary_symbols(child)
        elif isinstance(child, BinaryExpNode):
            child_type = self.eval_bin_expr_type(child)
        elif isinstance(child, RunNode):
            child_type = self.get_returnType_from_func(child)

        return child_type

    def type_w_higest_precedence(self, type_of_node, current_type=None):
        final_type = current_type

        if type_of_node == int and final_type is None:
            final_type = int
        elif type_of_node == float and final_type == int:
            final_type = float
        elif type_of_node == str and final_type != bool:
            final_type = str
        elif type_of_node == bool and final_type is None:
            final_type = bool

        return final_type

    def check_binExpr_exceptions(self, parent, lchild, rchild):

        if lchild == bool or rchild == bool:
            raise TypeError(parent, 'using booleans in binary expression assignment is illegal')
        elif not isinstance(parent, PlusNode):
            if lchild == str or rchild == str:
                raise TypeError(parent, 'is not allowed. Only plus with strings is allowed in expressions')

    def visit_FunctionNode(self, node):
        param_list = []
        self.current_scope.symbols[str(node.id.name + 'Node')] = node

        # Gets the formal parameters which is just the name of the formal input parameter.
        if node.params is not None:
            param_list = self.get_formal_params(node)

        self.current_scope.symbols[node.id.name] = param_list

    def populate_funcNode(self, node, scope, actual_param):
        outer_scope = scope
        inner_scope = scope.new_scope(scope)
        self.current_scope = inner_scope
        self.current_scope.symbols['returnType'] = 'void' # Puts in a return type "void" as default

        if node.params is not None:  # Adds the parameters to the scope
            self.add_params_to_scope(node, actual_param)

        node.block.visit_children(self)
        self.current_scope = outer_scope
        self.current_scope.symbols[str(node.id.name + 'Scope')] = inner_scope


    def get_formal_params(self, funcNode):
        param_list = []

        if isinstance(funcNode.params.id_list, list):
            for param in funcNode.params.id_list:
                param_list.append(param.name)

        return param_list

    def add_params_to_scope(self, funcNode, actual_param):
        if isinstance(funcNode.params.id_list, list):
            for (fparam, aparam) in zip(funcNode.params.id_list, actual_param):
                self.current_scope.symbols[fparam.name] = aparam

    def visit_WhenNode(self, node):
        self.visit_IfNode(node)

    def visit_IfNode(self, node):
        compare_operators = [EqualsNode, NotEqualNode, LessThanNode, GreaterThanNode, AndNode, OrNode]
        LHS_type_of_equal = None
        RHS_type_of_equal = None

        if isinstance(node.expression, BoolNode):
            pass
        elif isinstance(node.expression, IdNode):
            if self.current_scope.lookup(node.expression.name) != bool:
                raise TypeError(node.expression.name, 'is a not a boolean')
        elif isinstance(node.expression, RunNode):
            if self.get_returnType_from_func(node.expression) != bool:
                if isinstance(node.expression.id, DotNode):
                    raise TypeError(node.expression.id.ids, 'does not return a boolean. A function call that is not compared against anything has to return a boolean in when- and if-statements.')
                else:
                    raise TypeError(node.expression.id, 'does not return a boolean. A function call that is not compared against anything has to return a boolean in when- and if-statements.')
        elif type(node.expression) in compare_operators:
            # Evaluates the LHS of the compare operator
            if isinstance(node.expression.expr1, TermNode):
                LHS_type_of_equal = self.eval_term_node_type(node.expression.expr1)
            elif isinstance(node.expression.expr1, BinaryExpNode):
                LHS_type_of_equal = self.eval_bin_expr_type(node.expression.expr1)
            elif isinstance(node.expression.expr1, RunNode):
                LHS_type_of_equal = self.get_returnType_from_func(node.expression.expr1)
            elif isinstance(node.expression.expr1, UnaryExpNode):
                LHS_type_of_equal = self.ignore_unary_symbols(node.expression.expr1)


            # Evaluates the RHS of the compare operator
            if isinstance(node.expression.expr2, TermNode):
                RHS_type_of_equal = self.eval_term_node_type(node.expression.expr2)
            elif isinstance(node.expression.expr2, BinaryExpNode):
                RHS_type_of_equal = self.eval_bin_expr_type(node.expression.expr2)
            elif isinstance(node.expression.expr2, RunNode):
                RHS_type_of_equal = self.get_returnType_from_func(node.expression.expr2)
            elif isinstance(node.expression.expr2, UnaryExpNode):
                RHS_type_of_equal = self.ignore_unary_symbols(node.expression.expr2)

            if LHS_type_of_equal != RHS_type_of_equal:
                raise TypeError(LHS_type_of_equal, 'and', RHS_type_of_equal, 'is not the same and cannot be compared.')
        else:
            raise TypeError(type(node.expression), 'is not a legal type or compare operator in a when- or if-statement.')

        node.visit_children(self)

    def visit_ReturnNode(self, node):
        return_type = 'Void'

        if isinstance(node.expression, TermNode):
            return_type = self.eval_term_node_type(node.expression)
        elif isinstance(node.expression, BinaryExpNode):
            return_type = self.eval_bin_expr_type(node.expression)
        elif isinstance(node.expression, RunNode):
            return_type = self.get_returnType_from_func(node.expression)

        self.current_scope.symbols['returnType'] = return_type

    def visit_RunNode(self, node):
        # Type checks parameters and populate the funcNode if the run is a call to a sub-id. (LivingRoom.FunctionName).
        if isinstance(node.id, DotNode):
            self.dotNode_in_runNode(node)

        # Type checks parameters and pupulate the funcNode if the run is just an id.
        elif isinstance(node.id, IdNode):
            self.idNode_in_runNode(node)

    def idNode_in_runNode(self, idNode):
        cur_scope = self.current_scope
        formal_param = self.current_scope.lookup(idNode.id.name)
        actual_param = self.get_actual_params(idNode)

        if idNode.id.name in self.current_scope.predef_func_not_on_objects:
            pass
        elif len(formal_param) == len(actual_param):
            self.run_funcNode_and_typeCheck_params(formal_param, actual_param, idNode.id.name, cur_scope)
        else:
            raise TypeError(idNode.id.name, 'takes', len(self.current_scope.lookup(idNode.id.name)), 'parameter(s) and', len(self.get_actual_params(idNode)), 'was given.')

    def dotNode_in_runNode(self, runNode):
        last_id = runNode.id.ids[-1].name # Is the last name of a dot sequence like LivingRoom.light.setState
        cur_scope = self.current_scope

        for id in runNode.id.ids:
            # Checks if the last id is a built in function
            if self.current_scope.predefined_functions.get(last_id) is not None:
                if id.name == last_id:
                    formal_param = self.current_scope.predefined_functions.get(last_id)
                    actual_param = self.get_actual_params(runNode)

                    if (formal_param) != (actual_param):
                        raise TypeError(id.name, 'takes input', formal_param, 'and you gave it', actual_param)
                # Checks that the second last id is a predefined type
                elif id.name == runNode.id.ids[-2].name:
                    if self.current_scope.lookup(id.name) not in self.current_scope.predefined_types:
                        raise TypeError(id.name, 'is not one of the pre-defined object types: ', self.current_scope.predefined_types)
                else:
                    self.current_scope = self.current_scope.lookup(str(id.name + 'Scope'))
            # Takes the node of the last id instead of entering its scope
            elif id.name == last_id:
                formal_param = self.current_scope.lookup(id.name)
                actual_param = self.get_actual_params(runNode)

                if len(formal_param) == len(actual_param):
                    self.run_funcNode_and_typeCheck_params(formal_param, actual_param, id.name, cur_scope)
                else:
                    raise TypeError(id.name, 'takes', len(formal_param), 'parameter(s) and', len(actual_param), 'was given.')
            else:
                self.current_scope = self.current_scope.lookup(str(id.name + 'Scope'))

    def run_funcNode_and_typeCheck_params(self, formal_param, actual_param, id_name, cur_scope):
        list_of_types = [str, bool, int, float]

        if actual_param != []:
            if formal_param[0] not in list_of_types:  # Checks the first formal parameter is not a type
                self.call_funcNode(formal_param, actual_param, id_name, cur_scope)
            elif formal_param != actual_param:
                raise TypeError(id.name, 'takes input', formal_param, 'and you gave it', actual_param)
        else:  # Ellers bliver funktioner som open window ikke "bygget" fordi den ikke har input parameter
            self.populate_funcNode(self.current_scope.lookup(id.name + 'Node'), self.current_scope, actual_param)
            self.current_scope = cur_scope

    def call_funcNode(self, formal_param, actual_param, id_name, cur_scope):
        self.check_type_of_param_is_legal(formal_param, actual_param)
        # Change the scope to where the function is in.
        self.current_scope = self.current_scope.get_outer_scope_of_symbol(id_name)
        # Overwrites the formal params from e.g (x, y) to type of actual e.g (int, str)
        self.current_scope.symbols[id_name] = actual_param
        self.populate_funcNode(self.current_scope.lookup(id_name + 'Node'), self.current_scope, actual_param)
        # Sets the scope back to where it were before calling populate_funcnode
        self.current_scope = cur_scope

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

    def check_type_of_param_is_legal(self, formal_param, actual_param):
        list_of_types = [str, bool, int, float]

        assert all([aparam in list_of_types for aparam in actual_param])  # Checks all actual parameters has type
        assert all([fparam not in list_of_types for fparam in formal_param])  # Checks none of the formal parameters has a type