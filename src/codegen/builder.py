from src.codegen.control import Controller
from src.codegen.structures import Class, Method, Field

class Builder:
    def __init__(self):
        self.controller = Controller()


class MethodBuilder(Builder):

    def get_parameter(self, str1):
        parameter = None
        return parameter

    def get_statement(self, str1):
        pass

class FieldBuilder(Builder):
    pass


class ClassBuilder(Builder):

    def get_method(self, str1):
        method_builder = MethodBuilder()
        self.controller.setBuilder(method_builder)
        method = self.controller.getMethod(str1)
        return method

    def get_field(self, str1):
        field_builder = FieldBuilder()
        self.controller.setBuilder(field_builder)
        field = self.controller.getField(str1)
        return field


def main():
    class_builder = ClassBuilder()

    controller = Controller()
    class_str = "hello"
    #If class keyword is read:
    # Build class
    controller.setBuilder(class_builder)
    class1 = controller.getClass(class_str)
