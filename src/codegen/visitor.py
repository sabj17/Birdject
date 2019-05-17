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

class Visitor(NodeVisitor):

    def __init__(self, program, symtable):
        self.global_list = list()
        self.stack = Stack()
        self.func_used = True
        self.block_node_scopes = 1
        self.constructors = {}
        self.constructors_objects = {}
        self.setup_list = list()
        self.setup_objects = list()
        self.loop_list = list()
        self.current_classes = list()
        self.current_class = ""
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
            "OrNode" : " || ",
            "NotNode": " !",
            "NegativeNode": " -",
            "ParenthesesNode": ""
        }
        # self.structure = Structure(program)

    def setTable(self, symbtable):
        self.symtable = symbtable

    def get_tabs(self):
        tabs = 0
        if self.stack.top_of_stack() is "Global":
            tabs = 0
        elif self.stack.top_of_stack() is "When":
            tabs = 1
        elif self.stack.top_of_stack() is "GlobalFunction":
            tabs = 1
        else:
            tabs = 1

        return "" + tabs * "\t"


    def visit_ProgNode(self, node):
        self.setup_list.append("void setup() {\n\tSerial.begin(9600);")
        self.loop_list.append("void loop() {")
        self.stack.push("Global")
        # Stars visiting all nodes in the AST
        for node in node.stmts:
            node.accept(self)
        self.create_object_setup_func()
        self.setup_list.append("}\n")
        self.loop_list.append("}")

        file_std = open("resources/standard_classes.txt", "r")
        contents = file_std.read()
        program_file = open("resources/program.txt", "w")
        program_file.write(contents)


        for string in self.global_list:
            program_file.write(string + "\n")
        for string in self.setup_list:
            program_file.write(string + "\n")
        for string in self.loop_list:
            program_file.write(string + "\n")


        file_std.close()
        program_file.close()

        '''
        for string in self.global_list:
            print(string)
        for string in self.setup_list:
            print(string)
        for string in self.loop_list:
            print(string)
        '''

    def create_object_setup_func(self):
        string = "void setupObjects(){\n"
        for s in self.setup_objects:
            string += s
        string += "}\n"
        self.global_list.append(string)
        self.setup_list.append("\tsetupObjects();\n")

    def visit_ClassNode(self, node):
        class_name = node.id.accept(self)
        self.stack.push(class_name)
        old = self.current_class
        self.current_class = class_name
        self.current_classes.append(class_name)
        string = ""

        # Sets the scope in symbol table to be the class
        symtable_original = self.symtable
        self.setTable(self.symtable.lookup(class_name + "Scope"))

        # Creating the constructor and class assignment for the room
        self.constructors[class_name] = "\n" + self.get_tabs() + class_name + "Class()"
        self.constructors_objects[class_name] = 0
        string += "\n\nclass " + class_name + "Class {\n  public:\n"

        # Adds all of the body
        string += node.body_part.accept(self)

        # Ends the constructor and class
        self.constructors[class_name] += " {}\n"
        string += self.constructors[class_name] + "\n} " + class_name + ";\n"
        self.current_classes.remove(class_name)
        self.stack.pop()
        self.current_class = old

        # If not a sub class it is added to be global
        if self.stack.top_of_stack() == "Global":
            self.global_list.append(string)
        self.setTable(symtable_original)
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

        # var is already declared, so no type added
        if var_name in self.declared_vars:
            string += self.get_tabs() + var_name + " = " + expr_string
            # No semi colon added if expr is a runnode, since it is added in runnode visitor
            if not isinstance(node.expression, RunNode):
                string += ";"
            string += "\n"

        # Object assignment
        elif isinstance(node.expression, NewObjectNode):
            expr = node.expression
            object_name = expr.id.accept(self)
            params = expr.param.accept(self)

            # Global variable
            if self.stack.top_of_stack() == "Global":
                string += self.get_tabs() + object_name + " " + var_name + "(" + params + ");\n"
            # Declared inside a class
            else:
                string += self.get_tabs() + object_name + " " + var_name + ";\n"
                # Adding the object to the constructor of the room
                string_symbol = " : "
                if self.constructors_objects[self.current_class] > 0:
                    string_symbol = " , "
                self.constructors[self.current_class] += string_symbol + var_name + "(" + params + ")"
                self.constructors_objects[self.current_class] += 1

            # creates and adds the setupClass() func to the setupObjects func and calls that func in void setup()
            class_name = ""
            for name in self.current_classes:  # dot notation if needed
                class_name += name + "."
            self.setup_objects.append("\t" + class_name + var_name + ".setupClass();\n")

        # The cases where a new var with basic type is being declared
        else:
            var_type = self.symtable.lookup(var_name).__name__
            if var_type == 'str':
                string += self.get_tabs() + "String " + var_name + " = " + expr_string + ";\n"
            else: string += self.get_tabs() + var_type + " " + var_name + " = " + expr_string + ";\n"

        # Adds the variable to the list of declared variables
        self.declared_vars.append(var_name)
        node.expression.accept(self)

        # If global var dcl
        if self.stack.top_of_stack() == "Global":
            self.global_list.append(string)
        return string



    def visit_WhenNode(self, node):
        string = ""
        self.stack.push("When")

        # Setting the symbol table to be the block of 'when'
        original_symtable = self.symtable
        self.setTable(self.symtable.lookup("Block_scope" + str(self.block_node_scopes)))
        self.block_node_scopes += 1

        # Creates all the when stmt code
        expr = node.expression.accept(self)
        expr = self.replace_symbols(expr)
        string += "\n" + self.get_tabs() + "if (" + expr + "){\n"
        string += node.block.accept(self)
        string += self.get_tabs() + "}"

        # The code is added to the Arduino loop and symbol table is reset
        self.loop_list.append(string)
        self.setTable(original_symtable)
        self.stack.pop()

    def visit_NewObjectNode(self, node):
        id_string = node.id.accept(self)
        param_string = node.param.accept(self)
        return id_string + "(" + param_string + ")"


    def visit_FunctionNode(self, node):
        string = ""
        func_name = node.id.accept(self)

        # Global function
        if self.stack.top_of_stack() == "Global":
            self.stack.push("GlobalFunction")

        # Finds the function scope in symbol table
        symtable_original = self.symtable
        self.setTable(self.symtable.lookup(func_name + "Scope"))

        # Adds the parameters, if there is any
        func_params = ""
        if node.params is not None:
            func_params = node.params.accept(self)

        # Generates the function code
        string += "\n" + self.get_tabs() + "void " + func_name + " (" + func_params + "){\n"
        string += node.block.accept(self)
        string += self.get_tabs() + "}\n\n"
        self.setTable(symtable_original)

        # If func is called, the code for it is generated, otherwise not since the formal params have no type
        if self.func_used:
            if self.stack.top_of_stack() == "GlobalFunction":
                self.stack.pop()
                self.global_list.append(string)
            return string
        # Resets the func_used since the func was never used
        self.func_used = True
        return ""

    def visit_ReturnNode(self, node):
        return self.get_tabs() + "return " + node.expression.accept(self) + ";\n"

    def visit_FormalParameterNode(self, node):
        params = node.id_list
        param_amount = 0
        string = ""
        for param in params:
            # multiple parameters, so a ',' is added between
            if param_amount > 0:
                string += ", "
            param_name = param.accept(self)
            # If the type of the param is 'formalParam' then the function is never called, so 'func_used' is updated
            if self.symtable.lookup(param_name) == "formalParam":
                self.func_used = False
                return string
            # creates the string with the param type and name
            param_type = self.symtable.lookup(param_name).__name__
            if param_type == 'str':
                string += "String " + param_name
            else:
                string += param_type + " " + param_name
            param_amount += 1
        return string

    def visit_RunNode(self, node):
        string = ""
        # Justs sets tabs lul
        tabs = self.get_tabs()
        if self.stack.top_of_stack() == "Global":
            tabs = "\t"

        # Run is used via dot notation
        if isinstance(node.id, DotNode):
            string += tabs
            # iterates all the id's in the dot notation and adds a dot in between
            for index, dot_id in enumerate(node.id.ids):
                if index > 0:
                    string += "."
                string += dot_id.accept(self)
            string += "("
        # 'Normal' function is called
        else:
            if node.id.accept(self) == "print":
                string += tabs + "Serial.println("
            elif node.id.accept(self) == "await":
                string += tabs + "delay("
            else:
                string += tabs + node.id.accept(self) + "("

        # Adds params if there is any
        if node.params is not None:
            string += node.params.accept(self)
        string += ");\n"

        # if it is a globally called function, then it is added to setup() if its not in a when stmt
        if self.stack.top_of_stack() == "Global":
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
        string = ""
        true_block = node.statement_true
        false_block = node.statement_false
        expr = node.expression.accept(self)
        # Removes semi colon from expr in the case of it being a runnode
        expr = self.replace_symbols(expr)

        # Creates the 'if' stmt
        string += self.get_tabs() + "if (" + expr + ") {\n"
        string += self.create_if_body(true_block)

        # Creates the 'else if' stmt if needed
        if isinstance(false_block, IfNode):
            string += self.get_tabs() + "else "
            string += false_block.accept(self)

        # Creates the 'else' stmt if needed
        elif false_block is not None:
            string += self.get_tabs() + "else {\n"
            string += self.create_if_body(false_block)

        return string

    def create_if_body(self, block):
        string = block.accept(self)
        string = self.get_tabs() + string + self.get_tabs() + "}\n"
        return string

    def visit_BreakNode(self, node):
        return self.get_tabs() + "break;\n"


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
        string = string.replace("\t", "")
        return string