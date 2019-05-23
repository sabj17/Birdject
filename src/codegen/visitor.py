import os

from src.parser import Stack
from src.ast import BinaryExpNode, PlusNode, AbstractNode, NewObjectNode, IfNode, FormalParameterNode, DotNode, \
    AssignNode, UnaryExpNode, RunNode


class NodeVisitor:
    def visit(self, node):
        if isinstance(node, BinaryExpNode):
            method_name = 'visit_' + 'BinaryExpNode'
        elif isinstance(node, UnaryExpNode):
            method_name = 'visit_' + 'UnaryExpNode'
        else:
            method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)


class CodeGenVisitor(NodeVisitor):

    def __init__(self, symtable):
        self.table_stack = Stack()
        self.var_stack = Stack()
        self.class_stack = Stack()
        self.block_node_scopes = 1
        self.current_params = list()
        self.if_node_scopes = 1
        self.constructors = {}
        self.constructors_objects = {}
        self.global_list = list()
        self.setup_list = list()
        self.setup_objects = list()
        self.loop_list = list()
        self.current_class = ""
        self.declared_vars = set()
        self.symtable = symtable
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
            "OrNode" : " || ",
            "NotNode": " !",
            "NegativeNode": " -",
            "ParenthesesNode": ""
        }

    def push_scope(self, string):
        self.table_stack.push(self.lookup(string))
        self.var_stack.push(self.declared_vars)
        self.declared_vars.clear()

    def lookup(self, string):
        return self.table_stack.top_of_stack().lookup(string)

    def pop_scope(self):
        self.table_stack.pop()
        self.var_stack.pop()

    def setup(self):
        self.setup_list.append("void setup() {\nSerial.begin(9600);")
        self.loop_list.append("void loop() {")
        self.var_stack.push(self.declared_vars)
        self.table_stack.push(self.symtable)

    def end_code(self):
        self.create_object_setup_func()
        self.setup_list.append("}\n")
        self.loop_list.append("}")

    def code_gen(self, node, output_file):
        self.setup()

        # Starts visiting all nodes in the AST
        node.accept(self)

        self.end_code()

        # Writes the code to program.txt
        self.write_to_file(output_file)


    def write_to_file(self, output_file):
        # Opens the two txt files and reads from standard_classes
        file_std = open("resources/default_classes.txt", "r")
        contents = file_std.read()
        program_file = open(output_file, "w")
        program_file.write(contents)

        # All generated code is added to 'program.txt'
        for string in self.global_list:
            program_file.write(string + "\n")
        for string in self.setup_list:
            program_file.write(string + "\n")
        for string in self.loop_list:
            program_file.write(string + "\n")

        file_std.close()
        program_file.close()


    def visit_ProgNode(self, node):
        for node in node.stmts:
            node.accept(self)


    def create_object_setup_func(self):
        string = "void initializeObjects(){\n"
        for s in self.setup_objects:
            string += s
        string += "}\n"
        self.global_list.append(string)
        self.setup_list.append("initializeObjects();")

    def visit_ClassNode(self, node):
        class_name = node.id.accept(self)
        self.current_class = class_name
        self.class_stack.push(class_name)
        string = ""

        # Sets the scope in symbol table to be the class
        self.push_scope(class_name + "Scope")

        # Creating the constructor and class assignment for the room
        self.constructors[class_name] = "\n" + class_name + "Class()"
        self.constructors_objects[class_name] = 0
        string += "\n\nclass " + class_name + "Class {\n  public:\n"

        # Adds all of the body
        string += node.body_part.accept(self)

        # Ends the constructor and class
        self.constructors[class_name] += " {}\n"
        string += self.constructors[class_name] + "\n} " + class_name + ";\n"
        self.class_stack.pop()
        self.pop_scope()

        # If not a sub class it is added to be global
        if self.table_stack.size() == 1:
            self.global_list.append(string)
        return string

    def visit_ClassBodyNode(self, node):
        string = ""
        for part in node.body_parts:
            string += part.accept(self)
        return string

    def visit_BlockNode(self, node):
        string = ""
        for child in node.parts:
            string += child.accept(self)
        return string

    def visit_AssignNode(self, node):
        string = ""
        expr_string = node.expression.accept(self)
        var_name = node.id.accept(self)

        # var is already declared in current scope, so no type added
        if var_name in self.var_stack.top_of_stack() or var_name in self.current_params:
            string += self.create_var_assignment(var_name, expr_string, node)

        # Object declaration
        elif isinstance(node.expression, NewObjectNode):
            string += self.object_declaration(node, var_name)

        # The cases where a new var with basic type is being declared
        else:
            string += self.var_declaration(node, var_name, expr_string)
            # Adds the variable to the list of declared variables
            self.declared_vars.add(var_name)

        # Globally declared variable
        if self.table_stack.size() == 1:
            self.global_list.append(string)
        return string

    def create_var_assignment(self, var_name, expr_string, node):
        string = ""
        string += var_name + " = " + expr_string
        # No semi colon added if expr is a runnode, since it is added in runnode visitor
        if not isinstance(node.expression, RunNode):
            string += ";"
        string += "\n"
        return string

    def object_declaration(self, node, var_name):
        string = ""
        expr = node.expression
        object_name = expr.id.accept(self)
        params = expr.param.accept(self)

        # Object var declared outside a class has different syntax
        if self.table_stack.size() == 1:
            string += object_name + " " + var_name + "(" + params + ");\n"
        # Declared inside a class
        else:
            string += object_name + " " + var_name + ";\n"
            # Adding the object to the constructor of the room
            string_symbol = " : "
            if self.constructors_objects[self.current_class] > 0:
                string_symbol = " , "
            self.constructors[self.current_class] += string_symbol + var_name + "(" + params + ")"
            self.constructors_objects[self.current_class] += 1

        # creates and adds the initialize() func to the initializeObjects func and calls that func in void setup()
        class_name = ""
        for name in self.class_stack.items:  # dot notation if needed
            class_name += name + "."
        self.declared_vars.add(var_name)
        self.setup_objects.append(class_name + var_name + ".initialize();\n")
        return string

    def var_declaration(self, node, var_name, expr_string):
        string = ""
        var_type = self.lookup(var_name).__name__
        if var_type == 'str':
            string += "String " + var_name + " = " + expr_string + ";\n"
        else:
            string += var_type + " " + var_name + " = " + expr_string + ";\n"
        # Removes an extra semi colon, which would have been added if the expression is a RunNode
        if isinstance(node.expression, RunNode):
            string = self.replace_symbols(string)
            string += ";\n"
        return string

    def visit_WhenNode(self, node):
        string = ""

        # Setting the symbol table to be the block of 'when'
        self.push_scope("Block_scope" + str(self.block_node_scopes))
        self.block_node_scopes += 1

        # Creates all the 'when' stmt code
        expr = node.expression.accept(self)
        expr = self.replace_symbols(expr)
        string += "\n" + "if (" + expr + "){\n"
        string += node.block.accept(self)
        string += "}"

        # The code is added to the Arduino loop and symbol table is popped from the stack
        self.loop_list.append(string)
        self.pop_scope()

    def visit_NewObjectNode(self, node):
        id_string = node.id.accept(self)
        param_string = node.param.accept(self)
        return id_string + "(" + param_string + ")"


    def visit_FunctionNode(self, node):
        string = ""
        func_name = node.id.accept(self)

        # Finds the func scope in symbol table, if it doesnt exist, then it is never called and therefor not generated
        if not self.func_scope_exist(func_name):
            return ""

        # Gets the return type of the function
        return_type = self.get_return_type()

        # Adds the parameters, if there is any
        func_params = self.get_func_params(node)

        # Generates the function code and pops the function scope
        string += "\n" + return_type + " " + func_name + " (" + func_params + "){\n"
        string += node.block.accept(self)
        string += "}\n"
        self.pop_scope()

        # Global function
        if self.table_stack.size() == 1:
            self.global_list.append(string)
        self.current_params.clear()

        return string

    def get_func_params(self, node):
        func_params = ""
        if node.params is not None:
            func_params = node.params.accept(self)
        temp = func_params.replace("float", "")
        temp = temp.replace("int", "")
        temp = temp.replace("String", "")
        temp = temp.replace("bool", "")
        temp = temp.replace(" ", "")
        self.current_params = temp.split(",")
        return func_params

    def func_scope_exist(self, func_name):
        try:
            self.push_scope(func_name + "Scope")
            return True
        except NameError:
            return False

    def get_return_type(self):
        return_type = self.lookup("returnType")
        if not isinstance(return_type, str):
            return_type = self.lookup("returnType").__name__
        if return_type == 'str':
            return_type = "String"
        return return_type

    def visit_ReturnNode(self, node):
        return "return " + node.expression.accept(self) + ";\n"

    def visit_FormalParameterNode(self, node):
        params = node.id_list
        string = ""
        for index, param in enumerate(params):
            # multiple parameters, so a ',' is added between
            if index > 0:
                string += ", "
            param_name = param.accept(self)

            # creates the string with the param type and param name
            param_type = self.lookup(param_name).__name__
            if param_type == 'str':
                string += "String " + param_name
            else:
                string += param_type + " " + param_name
        return string

    def visit_RunNode(self, node):
        string = ""

        # Function called through dot notation
        if isinstance(node.id, DotNode):
            # iterates all the id's in the dot notation and adds a dot in between
            for index, dot_id in enumerate(node.id.ids):
                if index > 0:
                    string += "."
                string += dot_id.accept(self)
            string += "("

        # 'Normal' or standard function is called
        else:
            if node.id.accept(self) == "print":
                string += "Serial.println("
            elif node.id.accept(self) == "wait":
                string += "delay("
            else:
                string += node.id.accept(self) + "("

        # Adds params if there is any
        if node.params is not None:
            string += node.params.accept(self)
        string += ");\n"

        # A globally called function is added to setup()
        if self.table_stack.size() == 1:
            self.setup_list.append(string)

        return string

    def visit_ActualParameterNode(self, node):
        string = ""
        # iterates all the parameters
        for index, param in enumerate(node.expr_list):
            # Adds a comma in between params
            if index > 0:
                string += ", "
            temp_string = param.accept(self)
            # Removes ';' from the param if it is a run node
            if isinstance(param, RunNode):
                temp_string = self.replace_symbols(temp_string)
            string += temp_string
        return string

    def visit_IfNode(self, node):
        # Finds the if scope in symbol table
        self.table_stack.push(self.lookup("Block_scope" + str(self.if_node_scopes)))
        self.if_node_scopes += 1

        string = ""
        true_block = node.statement_true
        false_block = node.statement_false
        expr = node.expression.accept(self)
        # Removes semi colon from expr in the case of it being a runnode
        expr = self.replace_symbols(expr)

        # Creates the 'if' stmt
        string += "if (" + expr + ") {\n"
        string += self.create_if_body(true_block)

        # Creates the 'else if' stmt if needed
        if isinstance(false_block, IfNode):
            string += "else "
            string += false_block.accept(self)

        # Creates the 'else' stmt if needed
        elif false_block is not None:
            # Finds the scope for the else block
            self.table_stack.push(self.lookup("Block_scope" + str(self.if_node_scopes)))
            self.if_node_scopes += 1
            string += "else {\n"
            string += self.create_if_body(false_block)
            self.table_stack.pop()

        # Leaves the if scope symbol table and resets the scope counter for if blocks
        self.table_stack.pop()
        self.if_node_scopes = 1
        return string

    def create_if_body(self, block):
        string = block.accept(self)
        string = string + "}\n"
        return string

    def visit_BreakNode(self, node):
        return "break;\n"


    # Visitor method for all binary expressions
    def visit_BinaryExpNode(self, node):
        operator = self.operators[type(node).__name__]
        expr1 = node.expr1.accept(self)
        expr2 = node.expr2.accept(self)
        return expr1 + operator + expr2

    def visit_UnaryExpNode(self, node):
        operator = self.operators[type(node).__name__]
        expr = node.expression.accept(self)
        return operator + "(" + expr + ")"

    def visit_IntegerNode(self, node):
        return str(node.value)

    def visit_FloatNode(self, node):
        return str(node.value)

    def visit_StringNode(self, node):
        return "String(" + node.value + ")"

    def visit_BoolNode(self, node):
        if node.value == 'on':
            return "true"
        elif node.value == "off":
            return "false"
        return str(node.value)

    def visit_IdNode(self, node):
        return node.name

    def visit(self, node):
        return super().visit(node)

    def replace_symbols(self, string):
        string = string.replace(";", "")
        string = string.replace("\n", "")
        #string = string.replace("\t", "")
        return string