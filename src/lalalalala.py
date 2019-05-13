def eval_term_node_type(self, term_node):
    type_of_term_node = None

    print('bacon + 2', term_node)
    if isinstance(term_node, BoolNode):
        type_of_term_node = bool
    elif isinstance(term_node, IntegerNode):
        type_of_term_node = int
    elif isinstance(term_node, FloatNode):
        type_of_term_node = float
    elif isinstance(term_node, StringNode):
        type_of_term_node = str
    elif isinstance(term_node, IdNode):
        type_of_term_node = self.current_scope.lookup(term_node.name)

    print('looooooort', type_of_term_node)
    return type_of_term_node
