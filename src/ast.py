import random

from graphviz import Digraph, nohtml


class AST:
    def __init__(self, prog_node):
        self.prog = prog_node

    def accept(self, node_visitor):
        node_visitor.visit(self.prog)


class AbstractNode:

    def accept(self, node_visitor):
        return node_visitor.visit(self)


    def visit_children(self, node_visitor):
        for child in vars(self).values():
            if isinstance(child, list):  # if node has more than one child, the child variable will be a list
                for cc in child:
                    cc.accept(node_visitor)
            elif child is not None and not isinstance(child, str):
                child.accept(node_visitor)

    def __str__(self):
        return type(self).__name__


class ProgNode(AbstractNode):
    def __init__(self, stmts):
        super().__init__()
        self.stmts = stmts


##############
# STATEMENTS #
##############
class StatementNode(AbstractNode):
    pass


class IfNode(StatementNode):
    def __init__(self, expression, true, false):
        super().__init__()
        self.expression = expression
        self.statement_true = true
        self.statement_false = false


class WhenNode(StatementNode):
    def __init__(self, expression, block):
        super().__init__()
        self.expression = expression
        self.block = block


class ForNode(StatementNode):
    def __init__(self, id, expression, block):
        super().__init__()
        self.id = id
        self.expression = expression
        self.block = block


class AssignNode(StatementNode):
    def __init__(self, id, expression):
        super().__init__()
        self.id = id
        self.expression = expression


class FunctionNode(StatementNode):
    def __init__(self, id, params, block):
        super().__init__()
        self.id = id
        self.params = params
        self.block = block


class ClassNode(StatementNode):
    def __init__(self, id, body_part):
        super().__init__()
        self.id = id
        self.body_part = body_part


class ClassBodyNode(StatementNode):
    def __init__(self, body_parts):
        super().__init__()
        self.body_parts = body_parts


###############
# EXPRESSIONS #
###############
class ExpressionNode(AbstractNode):
    pass


class BinaryExpNode(ExpressionNode):
    def __init__(self, expr1, expr2):
        super().__init__()
        self.expr1 = expr1
        self.expr2 = expr2
        # Maybe have operand here instead of having many classes for it?


class UnaryExpNode(ExpressionNode):
    def __init__(self, expr):
        super().__init__()
        self.expression = expr


# UNARY EXPRESSIONS #
class NotNode(UnaryExpNode):
    def __init__(self, expr):
        super().__init__(expr)


class NegativeNode(UnaryExpNode):
    def __init__(self, expr):
        super().__init__(expr)


class ParenthesesNode(UnaryExpNode):
    def __init__(self, expr):
        super().__init__(expr)


class NewObjectNode(AbstractNode):
    def __init__(self, id, param):
        super().__init__()
        self.id = id
        self.param = param

    def __repr__(self):
        return self.id.__repr__() + "(" + self.param.__repr__() + ")"


# BINARY EXPRESSIONS #
class PlusNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " + " + self.expr2.__repr__()


class MinusNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " - " + self.expr2.__repr__()


class MultiplyNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " * " + self.expr2.__repr__()


class DivideNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " / " + self.expr2.__repr__()


class ModuloNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " % " + self.expr2.__repr__()


class EqualsNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " == " + self.expr2.__repr__()


class NotEqualNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " != " + self.expr2.__repr__()


class GreaterThanNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " > " + self.expr2.__repr__()


class LessThanNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " < " + self.expr2.__repr__()


class AndNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " && " + self.expr2.__repr__()


class OrNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)

    def __repr__(self):
        return self.expr1.__repr__() + " || " + self.expr2.__repr__()


###############
# BLOCK STUFF #
###############
class BlockNode(AbstractNode):
    def __init__(self, parts):
        super().__init__()
        self.parts = parts

class BlockBodyPartNode(AbstractNode):
    pass


class ReturnNode(BlockBodyPartNode):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class BreakNode(BlockBodyPartNode):
    pass


class RunNode(BlockBodyPartNode):
    def __init__(self, id, params):
        super().__init__()
        self.id = id
        self.params = params


###################
# PARAMETER STUFF #
###################
class ActualParameterNode(AbstractNode):
    def __init__(self, expr_list):
        super().__init__()
        self.expr_list = expr_list

    def __repr__(self):
        string = ""
        i = 0
        for child in self.expr_list:
            if isinstance(child, AbstractNode):
                if i > 0:
                    string += ", "
                string += child.__repr__()
                i += 1
        return string



class FormalParameterNode(AbstractNode):
    def __init__(self, id_list):
        super().__init__()
        self.id_list = id_list


##############
# TERM STUFF #
##############
class TermNode(AbstractNode):
    pass


class BoolNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return type(self).__name__ + ": " + str(self.value)

    def __repr__(self):
        if(self.value == 'on'):
            return "true"
        elif(self.value == "off"):
            return "false"
        return self.value + ""


class StringNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return type(self).__name__ + ": " + str(self.value)

    def __repr__(self):
        return self.value + ""


class FloatNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return type(self).__name__ + ": " + str(self.value)

    def __repr__(self):
        return self.value + ""


class IntegerNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return type(self).__name__ + ": " + str(self.value)

    def __repr__(self):
        return self.value + ""


class IdNode(TermNode):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return type(self).__name__ + ": " + str(self.name)

    def __repr__(self):
        return self.name


class DotNode(TermNode):
    def __init__(self, ids):
        super().__init__()
        self.ids = ids


class ArrayRefNode(TermNode):
    def __init__(self, id, index):
        super().__init__()
        self.id = id
        self.integer = index



class GraphASTVisitor:

    def __init__(self):
        self.parent = None
        self.graph = Digraph('G', node_attr={'style': 'filled'}, graph_attr={'ratio': 'fill', 'ranksep': '1.5'})


    def visit_children(self, node):
        children = vars(node).values()
        for child in children:
            if isinstance(child, list):
                for cc in child:
                    cc.accept(self)
            elif isinstance(child, AbstractNode):
                child.accept(self)

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        id = str(hash(node))
        self.graph.node(id, nohtml(str(node)))
        self.graph.edge(self.parent, id)

        parent = self.parent
        self.parent = id
        self.visit_children(node)
        self.parent = parent


    def visit_ProgNode(self, node):
        id = str(hash(node))
        self.graph.node(id, nohtml(str(node)))
        self.parent = id

        self.visit_children(node)

        self.graph.attr(overlap='false')
        self.graph.save(filename='AST.gv')