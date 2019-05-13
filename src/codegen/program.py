class Class(object):


    def
    def build_structure(self):
        pass


class Builder(object):
    def build(self, structure, id1):
        structure = object
        return Class()


class Program:
    def __init__(self):
        self.program = list()
        self.current_structure = None
        self.builder = Builder()

    def build_structure(self, structure, id1):
        if self.current_structure is None:
            self.current_structure = self.builder.build(structure, id1)
        else:
            self.current_structure.build_structure(structure)




class Program:
    def __init__(self):
        self.program = list()
        self.class_dcl = list()
        self.function_dcl = list()
        self.global_var_dcl = list()

        self.struct_stack = list()
        self.builder = Builder()


    def new_structure(self, structure, id1):
        structure = self.builder.get(structure, id1)
        if len(self.struct_stack) < 1:
            self.append_toplvl_struct(structure)
        self.struct_stack.append(structure)

    def end_structure(self, structure, id1):
        end_struct = self.struct_stack.pop()
        if not end_struct.verify(structure, id1):
            print("Exception: illegal struct end")
        else:
            TOS = self.struct_stack.index(len(self.struct_stack)-1)
            TOS.add_struct(end_struct)

    def append_toplvl_struct(self, structure):
        pass


class Structure:
    def __init__(self):
        self.struct_list = list()

    def add_struct(self, structure):
        self.struct_list.append(structure)































