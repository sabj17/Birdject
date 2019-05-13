
class Structure:
    def __init__(self):
        self.id = None
        self.structures = list()

    def add_id(self, id1):
        self.id = id1

    def add_structure(self, structure):
        self.structures.append(structure)

class Class(Structure):
    pass


class Builder(object):
    def getClass(self):
        class1 = Class()
        return class1


class Program:
    def __init__(self):
        #self.program = list()
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
        end_struct = self.TOS()
        if not end_struct.verify(structure, id1):
            print("Exception: illegal struct end")
        else:
            TOS = self.struct_stack.index(len(self.struct_stack)-1)
            TOS.add_struct(end_struct)


    def new_class(self):
        class1 = self.builder.getClass()
        self.struct_stack.append(class1)

    def emit_id(self, id1):
        structure = self.TOS()
        structure.add_id(id1)
        self.struct_stack.append(structure)

    def TOS(self):
        return self.struct_stack.pop()




    def new_non_structure(self):
        pass


    def append_toplvl_struct(self, structure):
        pass


class Structure:
    def __init__(self):
        self.struct_list = list()
        self.non_structs = list()

    def add_struct(self, structure):
        self.struct_list.append(structure)

    def add_non_struct(self, non_struct):
        self.non_structs.append(non_struct)


























