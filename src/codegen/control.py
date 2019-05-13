from src.codegen.strsplit import Splitter
from src.codegen.structures import Class, Method, Field


class Controller:
    __builder = None

    def __init__(self):
        self.splitter = Splitter()

    def setBuilder(self, builder):
        self.__builder = builder

    # CLASS STUFF#
    def getClass(self, str1):
        class_str = str1
        class1 = Class()

        name_str = self.splitter.get_class_name(class_str)
        class1.set_name(name_str)

        innerclasses_str = self.splitter.get_classes_str(class_str)
        for innerclass_str in innerclasses_str:
            inner_class = self.getClass(innerclass_str)
            class1.set_inner_class(inner_class)

        methods_str = self.splitter.get_methods_str(class_str)
        for method_str in methods_str:
            method = self.__builder.get_method(method_str)
            class1.set_method(method)

        fields_str = self.splitter.get_fields_str(class_str)
        for field_str in fields_str:
            field = self.__builder.get_field(field_str)
            class1.set_field(field)

        return class1

    # Method stuff#
    def getMethod(self, str1):
        method_str = str1
        method = Method()

        parameters_str = self.get_parameters(method_str)
        for parameter_str in parameters_str:
            parameter = self.__builder.get_parameter(parameter_str)
            method.set_parameter(parameter)

        statements_str = self.get_statements(method_str)
        for statement_str in statements_str:
            statement = self.__builder.get_statement(statement_str)
            method.set_statement(statement)

        return method

    def get_parameters(self, method_str):
        pass

    def get_statements(self, method_str):
        pass

    def getField(self, str1):
        pass