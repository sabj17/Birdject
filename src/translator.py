
class Translator:
    def __init__(self):
        self.global_scope = []
        self.loop_scope = []
        self.setup_scope = []

    def translate(self):
        pass

    def traverse_ast(self, ast):
        pass

    def get_children(self, node):
        children = []
        for childs in node:
            children.append(childs)
        return children