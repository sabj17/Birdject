class Structure:
    def __init__(self):
        self.id = None
        self.structures = list()
        self.otherstuff = list()

    def add_id(self, id1):
        self.id = id1

    def add_structure(self, structure):
        self.structures.append(structure)

    def add_vars(self, var):
        self.otherstuff.append(var)

    def get_id(self):
        return self.id

    def get_vars(self):
        return self.otherstuff

    def get_structures(self):
        return self.structures

    def get_self(self):
        pass

    def get_body(self):
        body = ""
        for var in self.get_vars():
            body += var
        for structure in self.get_structures():
             body += structure.get_self()
        return body


class Class(Structure):
    def get_self(self):
        dcl = "class " + self.get_id() + "{\n"
        body = self.get_body()
        return dcl + body + "\n};"


class Function(Structure):
    def __init__(self):
        super().__init__()
        self.params = list()
        self.return1 = None
        self.type1 = None

    def get_self(self):
        dcl = self.get_id()
        params = "(" + self.str_params() + "){\n"
        body = self.get_body()
        return dcl + params + body + "\n}"

    def str_params(self):
        params = None
        for param in self.params:
            params += param
        return params

    def add_params(self, params):
        self.params.append(params)

    def add_return(self, ret_expr, ret_type):
        self.return1 = ret_expr
        self.type1 = ret_type


class Builder(object):
    def getClass(self):
        class1 = Class()
        return class1

    def getFunction(self):
        function = Function()
        return function


class Program:
    def __init__(self):
        #self.program = list()
        self.class_dcl = list()
        self.function_dcl = list()
        self.global_var_dcl = list()

        self.struct_stack = Stack()
        self.builder = Builder()


    '''def new_structure(self, structure, id1):
        structure = self.builder.get(structure, id1)
        self.struct_stack.push(structure)
    '''
    def end_structure(self):
        end_struct = self.struct_stack.pop()
        if self.struct_stack.size() < 1:
            self.append_toplvl(end_struct)
        else:
            TOS = self.struct_stack.top_of_stack()
            TOS.add_structure(end_struct)


    def new_class(self):
        class1 = self.builder.getClass()
        self.struct_stack.push(class1)

    def new_function(self):
        function = self.builder.getFunction()
        self.struct_stack.push(function)


    def emit_id(self, id1):
        structure = self.struct_stack.top_of_stack()
        structure.add_id(id1)

    def emit_params(self, params):
        function = self.struct_stack.top_of_stack()
        function.add_params(params)

    def emit_non_structure(self, non_struct):
        if self.struct_stack.is_empty():
            self.global_var_dcl.append(non_struct)
        else:
            self.struct_stack.top_of_stack().add_vars(non_struct)


    def get_scope(self, symboltable):
        if self.struct_stack.is_empty():
            return None
        else:
            hello = symboltable
            for structure in self.struct_stack.items:
                hello = hello.lookup(structure.get_id()+"Scope")
            return hello


    def append_toplvl(self, structure):
        if isinstance(structure, Class):
            self.class_dcl.append(structure)
        elif isinstance(structure, Function):
            self.function_dcl.append(structure)


    def print(self):
        for var in self.global_var_dcl:
            print(var)
        for func in self.function_dcl:
            print(func)
        for class1 in self.class_dcl:
            print(class1.get_self())

'''
class Structure:
    def __init__(self):
        self.struct_list = list()
        self.non_structs = list()

    def add_struct(self, structure):
        self.struct_list.append(structure)

    def add_non_struct(self, non_struct):
        self.non_structs.append(non_struct)
'''





class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        return self.items.pop()

    def top_of_stack(self):
        return self.items[len(self.items)-1]

    def bottom_of_stack(self):
        return self.items[0]

    def __str__(self):
        return ", ".join([x.name for x in self.items])

    def size(self):
        return len(self.items)





















