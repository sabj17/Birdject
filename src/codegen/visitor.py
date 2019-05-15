from src.ast import BinaryExpNode, PlusNode, AbstractNode, NewObjectNode, IfNode, FormalParameterNode


class NodeVisitor:
    '''
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)

    '''
    def visit(self, node):
        if isinstance(node, BinaryExpNode):
            method_name = 'visit_' + 'BinaryExpNode'
        else:
            method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)




class Visitor(NodeVisitor):

    def __init__(self, program, symtable):
        # self.code_gen = CodeEmittor()'
        self.global_list = list()
        self.scope = 0
        self.setup_list = list()
        self.loop_list = list()
        self.current_string = ""
        self.class_constructor = ""
        self.objects_in_constructor = 0
        self.declared_vars = list()
        self.symtable = symtable
        self.program = program
        self.operators = {
            "PlusNode" : " + ",
            "MinusNode" : " - ",
            "MultiplyNode" : " * ",
            "DivideNode" : " / ",
            "ModuloNode" : " % ",
            "EqualsNode" : " == ",
            "NotEqualNode" : " != ",
            "GreaterThanNode" : " > ",
            "LessThanNode" : " < ",
            "AndNode" : " && ",
            "OrNode" : " || "
        }
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

    def add_scope(self):
        self.scope += 1

    def remove_scope(self):
        if self.scope > 0:
            self.scope -= 1
        else:
            self.scope = 0


    def reset_current(self):
        self.current_string = ""

    def reset_constructor(self):
        self.class_constructor = ""
        self.objects_in_constructor = 0

    def visit_ProgNode(self, node):
        self.setup_list.append("void setup() {\n\tSerial.begin(9600);")
        self.loop_list.append("void loop() {")
        statements = vars(node).get("stmts")
        for node in statements:
            node.accept(self)
        self.setup_list.append("}\n")
        self.loop_list.append("}")
        for string in self.global_list:
            print(string)
        for string in self.setup_list:
            print(string)
        for string in self.loop_list:
            print(string)


    def visit_IdNode(self, node):
        return node.name
        '''
        field = vars(node)
        key = field.keys()
        for k in key:
            self.program.emit_id(field.get(k)) '''

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
        class_name = super().visit(node.id)
        self.reset_constructor()
        if self.scope == 0:
            self.reset_current()

        # Sets the scope in symbol table to be the class
        symtableOriginal = self.symtable
        self.setTable(self.symtable.lookup(class_name + "Scope"))

        # Creating the constructor and class assignment for the room
        self.class_constructor += class_name + "Class()"
        self.add_scope()
        self.current_string += "\n\nclass " + class_name + "Class {\n  public:\n"
        self.add_scope()
        # Adds all of the body
        super().visit(node.body_part)
        self.remove_scope()
        # Ends the constructor and class
        self.class_constructor += " {}\n"
        self.current_string += self.class_constructor + "\n} " + class_name + ";\n"
        self.remove_scope()
        if self.scope == 0:
            self.global_list.append(self.current_string)
        self.setTable(symtableOriginal)


    def visit_ClassBodyNode(self, node):
        body_atb = vars(node)
        self.accept_children(body_atb.get("body_parts"))

    # Visitor method for all binary expressions
    def visit_BinaryExpNode(self, node):
        operator = self.operators[type(node).__name__]
        expr1 = super().visit(node.expr1)
        expr2 = super().visit(node.expr2)
        return expr1 + operator + expr2

    def visit_IntegerNode(self, node):
        return "" + node.value

    def visit_FloatNode(self, node):
        return "" + node.value

    def visit_StringNode(self, node):
        return "" + node.value

    def visit_BoolNode(self, node):
        if node.value == 'on':
            return "true"
        elif node.value == "off":
            return "false"
        return node.value + ""

    def visit_AssignNode(self, node):
        # If global var dcl
        if self.scope == 0:
            self.reset_current()

        expr_string = super().visit(node.expression)
        var_name = super().visit(node.id)

        if var_name in self.declared_vars:
            self.current_string += self.get_tabs() + var_name + " = " + expr_string + ";\n"

        # Object assignment
        elif isinstance(node.expression, NewObjectNode):
            expr = node.expression
            object_name = super().visit(expr.id)
            params = super().visit(expr.param)

            # Global variable
            if self.scope == 0:
                self.current_string += object_name + " " + var_name + "(" + params + ")\n"
            else:  # Declared inside a room
                self.current_string += self.get_tabs() + object_name + " " + var_name + ";\n"
                # Adding the object to the constructor of the room
                string_symbol = " : "
                if self.objects_in_constructor == 1:
                    string_symbol = " , "
                self.class_constructor += string_symbol + var_name + "(" + params + ")"
                self.objects_in_constructor += 1
            # adds the 'setupClass()' to void setup()
            self.setup_list.append("\t" + var_name + ".setupClass();")


        # The cases where a new var is being declared
        else:
            type1 = self.symtable.lookup(var_name).__name__
            if type1 == 'str':
                self.current_string += self.get_tabs() + "char " + var_name + "[100] = " + expr_string + ";\n"
            else: self.current_string += self.get_tabs() + type1 + " " + var_name + " = " + expr_string + ";\n"

        # Adds the variable to the list of declared variables
        self.declared_vars.append(var_name)

        self.accept_children(node.expression)

        # If global var dcl
        if self.scope == 0:
            self.global_list.append(self.current_string)


    def visit_FunctionNode(self, node):
        # Global function
        if self.scope == 0:
            self.reset_current()

        func_id = super().visit(node.id)
        # Adds the parameter to a string if there is any
        func_params = ""
        if node.params is not None:
            func_params = super().visit(node.params)

        # Finds the function scope in symbol table
        symtableOriginal = self.symtable
        self.setTable(self.symtable.lookup(func_id + "Scope"))
        # Generates the code
        self.current_string += "\n" + self.get_tabs() + "type " + func_id + " (" + func_params + "){\n"
        self.add_scope()
        super().visit(node.block)
        self.remove_scope()
        self.current_string += self.get_tabs() + "}\n\n"

        self.setTable(symtableOriginal)

        if self.scope == 0:
            self.global_list.append(self.current_string)


    def visit_ReturnNode(self, node):
        return_atb = vars(node)
        return_expr = return_atb.get("expression")
        self.current_string += self.get_tabs() + "return " + return_expr.__repr__() + ";\n"



    def visit_FormalParameterNode(self, node):
        param_atb = vars(node)
        param_amount = 0
        string = ""
        for param_list in param_atb.values():
            for param in param_list:
                if param_amount > 0:  # multiple parameters, so a ',' is added between
                    string += ", "
                string += "type " + super().visit(param)
                param_amount += 1
        return string

    # 'when' code is added to the loop
    def visit_WhenNode(self, node):
        expr = super().visit(node.expression)
        self.reset_current()
        self.add_scope()
        self.current_string += self.get_tabs() + "if (" + expr + "){\n"
        self.add_scope()
        self.add_scope()
        super().visit(node.block)
        self.remove_scope()
        self.remove_scope()
        self.current_string += self.get_tabs() + "}"
        self.loop_list.append(self.current_string)
        self.reset_current()

    def visit_NewObjectNode(self, node):
        id_string = super().visit(node.id)
        param_string = super().visit(node.param)
        return id_string + "(" + param_string + ")"


    def visit_RunNode(self, node):
        run_atb = vars(node)
        param = run_atb.get("params")

        # Justs sets tabs lul
        tabs = self.get_tabs()
        if self.scope == 0:
            self.reset_current()
            tabs = "\t"

        #TODO Check if id is dotnode

        # creates the function call code
        self.current_string += tabs + super().visit(node.id) + "("
        if param is not None:
            self.current_string += super().visit(node.params)
        self.current_string += ");\n"

        # if it is a globally called function, then it is added to setup()
        if self.scope == 0:
            self.setup_list.append(self.current_string)

    def visit_IfNode(self, node):
        true_block = node.statement_true
        false_block = node.statement_false
        # Global
        if self.scope == 0:
            self.reset_current()


        self.current_string += self.get_tabs() + "if (" + super().visit(node.expression) + ") {\n"
        self.create_if_body(true_block)
        if isinstance(false_block, IfNode):
            self.current_string += self.get_tabs() + "else "
            super().visit(false_block)
        elif false_block is not None:
            self.current_string += self.get_tabs() + "else {\n"
            self.create_if_body(false_block)








    def visit_ActualParameterNode(self, node):
        string = ""
        i = 0
        for child in node.expr_list:
            if isinstance(child, AbstractNode):
                if i > 0:
                    string += ", "
                string += super().visit(child)
                i += 1
        return string

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

    def create_if_body(self, block):
        self.add_scope()
        self.add_scope()
        super().visit(block)
        self.remove_scope()
        self.remove_scope()
        self.current_string += self.get_tabs() + "}\n"


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
