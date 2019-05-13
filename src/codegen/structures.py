class Class:
    def __init__(self):
        self.__name = ""
        self.__inner_classes = list()
        self.__methods = list()
        self.__fields = list()

    def set_field(self, field):
        self.__fields.append(field)

    def set_inner_class(self, class1):
        self.__inner_classes.append(class1)

    def set_method(self, method):
        self.__methods.append(method)

    def set_name(self, name_str):
        self.__name = name_str

    def specification(self):
        print("fields: %s" % self.__fields)
        print("methods: %d" % self.__methods)
        for class1 in self.__inner_classes:
            print("inner class: %s" % class1.specification())


class Method:
    def __init__(self):
        self.__parameters = list()
        self.__statements = list()

    def set_parameter(self, parameter):
        self.__parameters.append(parameter)

    def set_statement(self, statement):
        self.__statements.append(statement)


class Field:
    def __init__(self):
        self.__var_dcl = str()

    def set_var_dcl(self, dcl):
        self.__var_dcl = dcl


