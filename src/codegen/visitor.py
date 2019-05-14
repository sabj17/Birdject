from ast import BinaryExpNode, PlusNode, AbstractNode, NewObjectNode


class NodeVisitor:

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class Visitor(NodeVisitor):

    def __init__(self, program, symtable):
        # self.code_gen = CodeEmittor()'
        self.scope = 0
        self.global_string = ""
        self.setup_string = "void setup() {\n\tSerial.begin(9600);\n"
        self.loop_string = "void loop() {\n"
        self.current_string = ""
        self.class_constructor = ""
        self.objects_in_constructor = 0
        self.declared_vars = list()
        self.symtable = symtable
        self.program = program
        # self.structure = Structure(program)

    def setTable(self, symbtable):
        self.symtable = symbtable

    def get_tabs(self):
        tabs = 0
        if self.scope == 1:
            tabs = 1
        elif self.scope > 1:
            tabs = self.scope-1
        return "" + tabs * "\t"


    def reset_current(self):
        self.current_string = ""

    def reset_constructor(self):
        self.class_constructor = ""
        self.objects_in_constructor = 0

    def visit_ProgNode(self, node):
        statements = vars(node).get("stmts")
        for node in statements:
            node.accept(self)
        self.setup_string += "}\n\n"
        self.loop_string += "}\n\n"
        print("\n\n\n" + self.global_string + "\n\n" + self.setup_string + "\n" + self.loop_string)


    def visit_IdNode(self, node):
        field = vars(node)
        key = field.keys()
        for k in key:
            self.program.emit_id(field.get(k))

    def visit_BlockNode(self, node):
        block_atb = vars(node)
        parts = block_atb.get("parts")
        for child in parts:
            super().visit(child)

    def visit_BlockBodyPartNode(self, node):
        part_atb = vars(node)
        key = part_atb.keys()
        for k in key:
            print("part: " + part_atb.get(k))


    def visit_ClassNode(self, node):
        self.program.new_class()

        self.reset_constructor()
        class_atb = vars(node)
        class_id = class_atb.get("id")
        self.class_constructor += class_id.__repr__() + "Class"
        self.scope += 1
        self.global_string += "\n\nclass " + class_id.__repr__() + "Class {\n  public:\n"
        symtableOriginal = self.symtable
        self.setTable(self.symtable.lookup(class_id.__repr__() + "Scope"))
        self.scope += 1
        super().visit(class_atb.get("body_part"))
        self.scope -= 1
        self.class_constructor += " {}\n"
        self.setTable(symtableOriginal)
        self.global_string += self.class_constructor + "\n} " + class_id.__repr__() + ";\n"
        self.scope -= 1

    def visit_ClassBodyNode(self, node):
        body_atb = vars(node)
        self.reset_current()
        self.accept_children(body_atb.get("body_parts"))
        self.global_string += self.current_string

    def visit_AssignNode(self, node):
        if self.scope == 0:
            self.reset_current()
        assign_atb = vars(node)
        assign_id = assign_atb.get("id")
        expr = assign_atb.get("expression")
        if assign_id.__repr__() in self.declared_vars:
            self.current_string += self.get_tabs() + assign_id.__repr__() + " = " + expr.__repr__() + ";\n"
        elif self.symtable.lookup(assign_id.__repr__()) == int:
            self.current_string += self.get_tabs() + "int " + assign_id.__repr__() + " = " + expr.__repr__() + ";\n"
        elif self.symtable.lookup(assign_id.__repr__()) == float:
            self.current_string += self.get_tabs() + "float " + assign_id.__repr__() + " = " + expr.__repr__() + ";\n"
        elif self.symtable.lookup(assign_id.__repr__()) == bool:
            self.current_string += self.get_tabs() + "bool " + assign_id.__repr__() + " = " + expr.__repr__() + ";\n"
        elif self.symtable.lookup(assign_id.__repr__()) == str:
            self.current_string += self.get_tabs() + "char " + assign_id.__repr__() + "[100] = " + expr.__repr__() + ";\n"
        # Object assignment
        elif isinstance(expr, NewObjectNode):
            obj_atb = vars(expr)
            obj_id = obj_atb.get("id")
            obj_param = obj_atb.get("param")
            # Global variable
            if(self.scope == 0):
                self.current_string += obj_id.__repr__() + " " + assign_id.__repr__() + "(" + obj_param.__repr__() + ")"
            else: #Declared inside a room
                self.current_string += self.get_tabs() + obj_id.__repr__() + " " + assign_id.__repr__() + ";\n"
                # Adding the object to the constructor of the room
                string_symbol = " : "
                if self.objects_in_constructor == 1:
                    string_symbol = " , "
                self.class_constructor += string_symbol + assign_id.__repr__() + "(" + obj_param.__repr__() + ")"
                self.objects_in_constructor += 1
            # adds the 'setupClass()' to void setup()
            self.setup_string += "\t" + assign_id.__repr__() + ".setupClass();\n"
        self.declared_vars.append(assign_id.__repr__())


        #   self.code_gen.emit_id(assign_id)
        self.accept_children(assign_atb.get("expression"))

        if self.scope == 0:
            self.global_string += self.current_string
        return self.current_string

    def visit_FunctionNode(self, node):
        if self.scope == 0:
            self.reset_current()
        function_atb = vars(node)
        function_id = function_atb.get("id")
        function_params = function_atb.get("params")
        function_block = function_atb.get("block")
        symtableOriginal = self.symtable
        self.setTable(self.symtable.lookup(function_id.__repr__() + "Scope"))
        self.current_string += "\n" + self.get_tabs() + "type " + function_id.__repr__() + " ("
        if function_params is not None:
            super().visit(function_params)
        self.current_string += "){\n"
        self.scope += 1
        super().visit(function_block)
        self.scope -= 1
        self.current_string += self.get_tabs() + "}\n\n"
        self.setTable(symtableOriginal)

        if self.scope == 0:
            self.global_string += self.current_string


    def visit_ReturnNode(self, node):
        return_atb = vars(node)
        return_expr = return_atb.get("expression")
        self.current_string += self.get_tabs() + "return " + return_expr.__repr__() + ";\n"


    def visit_FormalParameterNode(self, node):
        param_atb = vars(node)
        i = 0
        for param_list in param_atb.values():
            for param in param_list:
                if i > 0:
                    self.current_string += ", "
                self.current_string += "type " + param.__repr__()
                i += 1

    def visit_WhenNode(self, node):
        when_atb = vars(node)
        when_expr = when_atb.get("expression")
        when_block = when_atb.get("block")
        self.current_string = self.loop_string
        self.scope += 1
        self.current_string += self.get_tabs() + "if ("
        self.current_string += when_expr.__repr__() + "){\n"
        self.scope += 2
        super().visit(when_block)
        self.scope -= 2
        self.current_string += self.get_tabs() + "}\n"
        self.loop_string = self.current_string
        self.reset_current()

    def visit_NewObjectNode(self, node):
        object_atb = vars(node)
        param = object_atb.get("param")
        object_id = object_atb.get("id")
        super().visit(param)



    def visit_ActualParameterNode(self, node):
        param_atb = vars(node)

        '''
        i = 0
        for param_list in param_atb.values():
            for param in param_list:
                if i > 0:
                    self.current_string += ", "
                self.current_string += "type " + param.__repr__()
                i += 1
'''

    def visit(self, node):
        super().visit(node)

    def accept_children(self, children):
        if isinstance(children, AbstractNode):
            super().visit(children)
            # children.accept(self)
        elif isinstance(children, list):
            for child in children:
                super().visit(child)
                # child.accept(self)


'''
class TopVisitor(NodeVisitor):

    def __init__(self, program):
        self.code_gen = CodeEmittor()
        self.program = program
        self.structure = Structure(program)

    @dispatch(ProgNode)
    def visit(self, node):
        self.structure.begin_structure()
        statements = vars(node).get("stmts")
        for node in statements:
            node.accept(self)

    @dispatch(ClassNode)
    def visit(self, node):
        class_atb = vars(node)
        class_id = class_atb.get("id")
        self.code_gen.emit_class_name(class_id)
        self.accept_children(class_id, class_atb.get("body_part"))

    @dispatch(FunctionNode)
    def visit(self, node):
        function_atb = vars(node)
        function_id = function_atb.get("id")
        function_params = function_atb.get("params")
        function_block = function_atb.get("block")

        self.code_gen.emit_func()
        function_id.accept(self)
        function_params.accept(self)
        self.accept_children(function_id, function_block)

    @dispatch(AssignNode)
    def visit(self, node):
        assign_atb = vars(node)
        assign_id = assign_atb.get("id")
        self.code_gen.emit_id(assign_id)
        self.accept_children(assign_id, assign_atb.get("expression"))

    @dispatch(RunNode)
    def visit(self, node):
        self.code_gen.emit_run()
        run_atb = vars(node)
        run_id = run_atb.get("id")
        run_params = run_atb.get("params")
        run_id.accept(self)
        if run_params is not None:
            run_params.accept(self)
        self.code_gen.emit_end("function_call")


    @dispatch(IfNode)
    def visit(self, node):
        if_atb = vars(node)
        if_true = if_atb.get("statement_true")
        if_false = if_atb.get("statement_false")
        self.code_gen.emit_if_vals(if_true, if_false)
        self.accept_children("if", if_atb.get("expression"))

    @dispatch(ForNode)
    def visit(self, node):
        for_atb = vars(node)
        for_id = for_atb.get("id")
        self.accept_children(for_id, for_atb.get("expression"))
        self.accept_children(for_id, for_atb.get("block"))

    @dispatch(WhenNode)
    def visit(self, node):
        when_atb = vars(node)
        self.accept_children("When", when_atb.get("expression"))
        self.accept_children("When", when_atb.get("block"))

    @dispatch(BlockNode)
    def visit(self, node):
        block_atb = vars(node)
        parts = block_atb.get("parts")
        for child in parts:
            child.accept(self)

    @dispatch(BlockBodyPartNode)
    def visit(self, node):
        self.code_gen.emit_block_body()

    @dispatch(ActualParameterNode) #hello
    def visit(self, node):
        self.code_gen.emit_parameters()
        expr_list = vars(node).get("expr_list")
        for child in expr_list:
            child.accept(self)
        self.code_gen.emit_end("Param")

    @dispatch(ExpressionNode)
    def visit(self, node):
        self.code_gen.emit_expression()

    @dispatch(BinaryExpNode)
    def visit(self, node):
        self.code_gen.emit_binary_exp()

    @dispatch(UnaryExpNode)
    def visit(self, node):
        self.code_gen.emit_unary_exp()

    @dispatch(NotNode)
    def visit(self, node):
        self.code_gen.emit_not_exp()

    @dispatch(NegativeNode)
    def visit(self, node):
        self.code_gen.emit_negative_exp()

    @dispatch(ParenthesesNode)
    def visit(self, node):
        self.code_gen.emit_paren_exp()

    @dispatch(NewObjectNode)
    def visit(self, node):
        self.code_gen.emit_new_obj_exp()

    @dispatch(PlusNode)
    def visit(self, node):
        self.code_gen.emit_plus_exp()
        expr = vars(node)
        for key in expr.keys():
            expr.get(key).accept(self)
        self.code_gen.emit_end("plus_exp")

    @dispatch(MinusNode)
    def visit(self, node):
        self.code_gen.emit_minus_exp()

    @dispatch(MultiplyNode)
    def visit(self, node):
        self.code_gen.emit_mult_exp()

    @dispatch(DivideNode)
    def visit(self, node):
        self.code_gen.emit_div_exp()

    @dispatch(ModuloNode)
    def visit(self, node):
        self.code_gen.emit_mod_exp()

    @dispatch(EqualsNode)
    def visit(self, node):
        self.code_gen.emit_equals_exp()

    @dispatch(NotEqualNode)
    def visit(self, node):
        self.code_gen.emit_not_equals_exp()

    @dispatch(GreaterThanNode)
    def visit(self, node):
        self.code_gen.emit_greater_than_exp()

    @dispatch(LessThanNode)
    def visit(self, node):
        self.code_gen.emit_less_than_exp()

    @dispatch(AndNode)
    def visit(self, node):
        self.code_gen.emit_and_exp()

    @dispatch(OrNode)
    def visit(self, node):
        self.code_gen.emit_or_exp()

    @dispatch(IdNode)
    def visit(self, node):
        field = vars(node)
        key = field.keys()
        for k in key:
            self.code_gen.emit_id(field.get(k))

    ##############
    # TERM STUFF #
    ##############

    @dispatch(TermNode)
    def visit(self, node):
        self.code_gen.emit_terminal()

    @dispatch(BoolNode)
    def visit(self, node):
        self.code_gen.emit_bool()

    @dispatch(StringNode)
    def visit(self, node):
        self.code_gen.emit_string()

    @dispatch(FloatNode)
    def visit(self, node):
        self.code_gen.emit_float()

    @dispatch(IntegerNode)
    def visit(self, node):
        field = vars(node)
        self.code_gen.emit_integer(field.get("value"))

    @dispatch(DotNode)
    def visit(self, node):
        self.code_gen.emit_dot()
        ids = vars(node).get("ids")
        for id1 in ids:
            id1.accept(self)
        self.code_gen.emit_end("dot")

    @dispatch(ArrayRefNode)
    def visit(self, node):
        self.code_gen.emit_array_ref()

    @dispatch(object)
    def visit(self, node):
        pass

    def accept_children(self, cnode_id, children):
        if isinstance(children, AbstractNode):
            children.accept(self)
        elif isinstance(children, list):
            for child in children:
                child.accept(self)
        self.code_gen.emit_end(cnode_id)

'''

'''
class CodeGenVisitor(NodeVisitor):

    def __init__(self):
        self.code_gen = CodeEmittor()

    @dispatch(ProgNode)
    def visit(self, node):
        self.code_gen.emit_prog()

    @dispatch(object)
    def visit(self, node):
        pass

    ##############
    # STATEMENTS #
    ##############

    @dispatch(StatementNode)
    def visit(self, node):
        self.code_gen.emit_statement()

    @dispatch(IfNode)
    def visit(self, node):
        self.code_gen.emit_if()

    @dispatch(WhenNode)
    def visit(self, node):
        self.code_gen.emit_when()

    @dispatch(ForNode)
    def visit(self, node):
        self.code_gen.emit_for()

    @dispatch(AssignNode)
    def visit(self, node):
        self.code_gen.emit_assign()

    @dispatch(FunctionNode)
    def visit(self, node):
        self.code_gen.emit_func()

    @dispatch(ClassNode)
    def visit(self, node):
        self.code_gen.emit_class()

    @dispatch(ClassBodyNode)
    def visit(self, node):
        self.code_gen.emit_class_body()

    ###############
    # EXPRESSIONS #
    ###############

    @dispatch(ExpressionNode)
    def visit(self, node):
        self.code_gen.emit_expression()

    @dispatch(BinaryExpNode)
    def visit(self, node):
        self.code_gen.emit_binary_exp()

    @dispatch(UnaryExpNode)
    def visit(self, node):
        self.code_gen.emit_unary_exp()

    @dispatch(NotNode)
    def visit(self, node):
        self.code_gen.emit_not_exp()

    @dispatch(NegativeNode)
    def visit(self, node):
        self.code_gen.emit_negative_exp()

    @dispatch(ParenthesesNode)
    def visit(self, node):
        self.code_gen.emit_paren_exp()

    @dispatch(NewObjectNode)
    def visit(self, node):
        self.code_gen.emit_new_obj_exp()

    @dispatch(PlusNode)
    def visit(self, node):
        self.code_gen.emit_plus_exp()

    @dispatch(MinusNode)
    def visit(self, node):
        self.code_gen.emit_minus_exp()

    @dispatch(MultiplyNode)
    def visit(self, node):
        self.code_gen.emit_mult_exp()

    @dispatch(DivideNode)
    def visit(self, node):
        self.code_gen.emit_div_exp()

    @dispatch(ModuloNode)
    def visit(self, node):
        self.code_gen.emit_mod_exp()

    @dispatch(EqualsNode)
    def visit(self, node):
        self.code_gen.emit_equals_exp()

    @dispatch(NotEqualNode)
    def visit(self, node):
        self.code_gen.emit_not_equals_exp()

    @dispatch(GreaterThanNode)
    def visit(self, node):
        self.code_gen.emit_greater_than_exp()

    @dispatch(LessThanNode)
    def visit(self, node):
        self.code_gen.emit_less_than_exp()

    @dispatch(AndNode)
    def visit(self, node):
        self.code_gen.emit_and_exp()

    @dispatch(OrNode)
    def visit(self, node):
        self.code_gen.emit_or_exp()

    ###############
    # BLOCK STUFF #
    ###############

    @dispatch(BlockNode)
    def visit(self, node):
        self.code_gen.emit_block()

    @dispatch(BlockBodyPartNode)
    def visit(self, node):
        self.code_gen.emit_block_body()

    @dispatch(ReturnNode)
    def visit(self, node):
        self.code_gen.emit_return()

    @dispatch(BreakNode)
    def visit(self, node):
        self.code_gen.emit_break()

    @dispatch(RunNode)
    def visit(self, node):
        self.code_gen.emit_run()

    ###################
    # PARAMETER STUFF #
    ###################

    @dispatch(ActualParameterNode)
    def visit(self, node):
        self.code_gen.emit_parameters()

    ##############
    # TERM STUFF #
    ##############

    @dispatch(TermNode)
    def visit(self, node):
        self.code_gen.emit_terminal()

    @dispatch(BoolNode)
    def visit(self, node):
        self.code_gen.emit_bool()

    @dispatch(StringNode)
    def visit(self, node):
        self.code_gen.emit_string()

    @dispatch(FloatNode)
    def visit(self, node):
        self.code_gen.emit_float()

    @dispatch(IntegerNode)
    def visit(self, node):
        field = vars(node)
        self.code_gen.emit_integer(field.get("value"))

    @dispatch(IdNode)
    def visit(self, node):
        field = vars(node)
        key = field.keys()
        for k in key:
            self.code_gen.emit_id(field.get(k))

    @dispatch(DotNode)
    def visit(self, node):
        self.code_gen.emit_dot()

    @dispatch(ArrayRefNode)
    def visit(self, node):
        self.code_gen.emit_array_ref()
'''
