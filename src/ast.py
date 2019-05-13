import random
from graphviz import Digraph, nohtml



class AST:
    def __init__(self, prog_node):
        self.prog = prog_node


    def graph(self):
        graph = Digraph('G', node_attr={'style': 'filled'}, graph_attr={'ratio': 'fill', 'ranksep': '1.5'})
        graph.attr(overlap='false')
        self.prog.graph(graph)
        graph.save(filename='AST.gv')

    def accept(self, visitor):
        return self.prog.accept(visitor)


class AbstractNode:

    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.__str__()))
        if parent:
            graph.edge(parent, id)

        class_vars = vars(self)
        for child in class_vars.values():
            if isinstance(child, AbstractNode):
                child.graph(graph, id)
            else:
                if child:
                    id2 = str(random.randint(1, 10000000))
                    # print(child, self.__class__.__name__)
                    graph.node(id2, nohtml(child))
                    graph.edge(id, id2)

    def has_children(self):
        for child in vars(self).values():
            if isinstance(child, AbstractNode):
                return True
        return False


    def accept(self, node_visitor):
        node_visitor.visit(self)

    '''def accept(self, node_visitor):
        node_visitor.visit(self)
        class_vars = vars(self)
        varz=[]
        for value in class_vars.values():
            varz.append(value)
        for child in varz:
            if isinstance(child, AbstractNode):
                child.accept(node_visitor)
            elif isinstance(child, list):
                for s_child in child:
                    s_child.accept(node_visitor)
    '''


    '''def accept(self, node_visitor):
        class_vars = vars(self)
        varz = []
        for value in class_vars.values():
            varz.append(value)
        for child in reversed(varz):
            if isinstance(child, AbstractNode):
                child.accept(node_visitor)
            elif isinstance(child, list):
                for s_child in child:
                    s_child.accept(node_visitor)

        #node_visitor.visit(self)
    '''
    def __str__(self):
        return type(self).__name__


class ProgNode(AbstractNode):
    def __init__(self, stmts):
        super().__init__()
        self.stmts = stmts

    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.__str__()))

        for stmt in self.stmts:
            stmt.graph(graph, id)


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
    def __init__(self, id1, expression, block):
        super().__init__()
        self.id = id1
        self.expression = expression
        self.block = block


class AssignNode(StatementNode):
    def __init__(self, id1, expression):
        super().__init__()
        self.id = id1
        self.expression = expression


class FunctionNode(StatementNode):
    def __init__(self, id1, params, block):
        super().__init__()
        self.id = id1
        self.params = params
        self.block = block


class ClassNode(StatementNode):
    def __init__(self, id1, body_part):
        super().__init__()
        self.id = id1
        self.body_part = body_part
        self.end = EndNode()


class ClassBodyNode(StatementNode):
    def __init__(self, body_parts):
        super().__init__()
        self.body_parts = body_parts


    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.__str__()))
        if parent:
            graph.edge(parent, id)

        for child in self.body_parts:
            if isinstance(child, AbstractNode):
                child.graph(graph, id)


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


# BINARY EXPRESSIONS #
class PlusNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class MinusNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class MultiplyNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class DivideNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class ModuloNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class EqualsNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class NotEqualNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class GreaterThanNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class LessThanNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class AndNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class OrNode(BinaryExpNode):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


###############
# BLOCK STUFF #
###############
class BlockNode(AbstractNode):
    def __init__(self, parts):
        super().__init__()
        self.parts = parts


    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.__str__()))
        if parent:
            graph.edge(parent, id)

        for child in self.parts:
            if isinstance(child, AbstractNode):
                child.graph(graph, id)


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
class ParameterNode(AbstractNode):
    def __init__(self, expr_list):
        super().__init__()
        self.expr_list = expr_list

    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.__str__()))
        if parent:
            graph.edge(parent, id)

        for child in self.expr_list:
            if isinstance(child, AbstractNode):
                child.graph(graph, id)


##############
# TERM STUFF #
##############
class TermNode(AbstractNode):
    pass


class BoolNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class StringNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class FloatNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IntegerNode(TermNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IdNode(TermNode):
    def __init__(self, name):
        super().__init__()
        self.name = name


class DotNode(TermNode):
    def __init__(self, ids):
        super().__init__()
        self.ids = ids

    def graph(self, graph, parent=None):
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.__str__()))
        if parent:
            graph.edge(parent, id)

        for child in self.ids:
            if isinstance(child, AbstractNode):
                child.graph(graph, id)


class ArrayRefNode(TermNode):
    def __init__(self, id, index):
        super().__init__()
        self.id = id
        self.integer = index


class EndNode(AbstractNode):
    def __init__(self):
        pass