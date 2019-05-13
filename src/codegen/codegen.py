
class CodeGenerator:
    def __init__(self):
        self.program = []
        self.classes = []
        self.functions = []
        self.code = []


    class Controller:
        def __init__(self):
            self.current_structure = None

        def set_current_structure(self, structure):
            self.current_structure

    def controller(self):
        current_structure


    class Class:
        def __init__(self):
            pass



    def classBuilder(self):
        pass























    class Class:
        def __init__(self):
            self.name = None
            self.fields = []
            self.body = []

        def add_field(self, field):
            self.fields.append(field)
            return self

        def set_name(self, name):
            self.name = name
            return self

        def add_body_part(self, part):
            self.body.append(part)
            return self

    class Function:
        def __init__(self, name, body):
            self.name = name
            self.body = body

    def build_class(self, class_atr):
        name = class_atr
        self.classes.append(self.Class().set_name())













    def builder(self, inp):
        self.code.append(inp)
        if inp == "end":
            self.close_structure()


    def class_(self):
        pass

    def build_function(self):
        func = self.code
        function = []
        for code in reversed(func):
            function.append(code)
            if code == "end":
                break
        return function

    def program(self):
        pass

    def end(self):
        pass

    def close_structure(self):
        structure = []
        for word in self.code:
            structure.append(word)
            if word == "Function":
                self.functions.append(structure)
                self.code = []
        print("Functions: ")
        print(self.functions)
        print("code: ")
        print(self.code)




class CodeEmittor:

    def __init__(self):
        self.targetCode = []
        self.first = [] #Global var dcls and class dcls
        self.middle = [] #Setup and loop
        self.last = [] #Function dcls
        self.classnr = 0
        self.scope = None
        self.stack = []
        self.codegen = CodeGenerator()

    def generate_tcode(self):
        #print(self.codegen.functions)
        pass


    def emit_class(self):
        self.stack.append("class")
        self.codegen.builder("class")
        self.scope = "class"+str(self.classnr)
        self.classnr += 1

    def emit_id(self, value):
        self.codegen.builder(value)


    def emit_class_body(self):
        self.stack.append("Class_body")
        self.codegen.builder("Class_body")

    def emit_global_var(self):
        pass

    def emit_prog(self):
        self.stack.append("Prog")
        self.codegen.builder("Prog")

    def emit_terminal(self):
        self.stack.append("Terminal")
        self.codegen.builder("Terminal")

    def emit_func(self):
        self.stack.append("Function")
        self.codegen.builder("Function")

    def emit_assign(self):
        pass

    def emit_for(self):
        pass

    def emit_when(self):
        pass

    def emit_if(self):
        pass

    def emit_statement(self):
        self.codegen.builder("stmt")

    def emit_expression(self):
        self.stack.append("exp")
        self.codegen.builder("exp")

    def emit_binary_exp(self):
        self.codegen.builder("binary_exp")

    def emit_unary_exp(self):
        self.codegen.builder("unary_exp")

    def emit_not_exp(self):
        self.codegen.builder("not_exp")

    def emit_negative_exp(self):
        pass

    def emit_paren_exp(self):
        self.codegen.builder("paren_exp")

    def emit_new_obj_exp(self):
        pass

    def emit_plus_exp(self):
        self.stack.append("plus_exp")
        self.codegen.builder("plus_exp")

    def emit_minus_exp(self):
        pass

    def emit_mult_exp(self):
        pass

    def emit_div_exp(self):
        pass

    def emit_mod_exp(self):
        pass

    def emit_equals_exp(self):
        pass

    def emit_not_equals_exp(self):
        pass

    def emit_greater_than_exp(self):
        pass

    def emit_less_than_exp(self):
        pass

    def emit_and_exp(self):
        pass

    def emit_or_exp(self):
        pass

    def emit_block(self):
        self.stack.append("block")
        self.codegen.builder("block")

    def emit_block_body(self):
        self.stack.append("block body")
        self.codegen.builder("block body")

    def emit_return(self):
        pass

    def emit_break(self):
        pass

    def emit_run(self):
        self.codegen.builder("function_call")

    def emit_parameters(self):
        self.codegen.builder("parameters:")

    def emit_bool(self):
        pass

    def emit_string(self):
        pass

    def emit_float(self):
        pass

    def emit_integer(self, value):
        self.stack.append(value)
        self.codegen.builder(value)

    def emit_dot(self):
        self.stack.append(".")
        self.codegen.builder("dot")

    def emit_array_ref(self):
        pass

    def emit_end(self, id1):
        self.codegen.builder(id1)
        self.codegen.builder("end")

    def emit_class_name(self, class_id):
        self.stack.append(class_id)

    def emit_if_vals(self, if_true, if_false):
        self.stack.append("if")
        if if_true:
            self.stack.append("TRUE")
        else:
            self.stack.append("FALSE")



