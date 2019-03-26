class Node:

    def __init__(self, value):
        self.children = []
        self.value = value
        # self.children = children
        self.is_leaf = False
        self.index = 0

    def is_a_leaf(self, bool):
        self.is_leaf = bool

    def add_child(self, child):
        self.children.append(child)

    def has_more_children(self):
        if len(self.children) > self.index + 1:
            return True
        return False

    def next_child(self):
        if self.has_more_children():
            return self.children[self.index + 1]
        return None

    def get_child_with_name(self, name):
        for child in self.children:
            if child.value.name == name:
                print(self.value.name + ": " + child.value.name)
                return child

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value.name)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        if self.is_leaf:
            return self.value.name
        return self.value.name