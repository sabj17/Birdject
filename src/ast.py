class AbstractNode:

    def __init__(self):
        pass


###############
# STATEMENTS #
###############
class StatementNode(AbstractNode):
    pass


class IfStmtNode(StatementNode):
    pass


class WhenStmtNode(StatementNode):
    pass


class ForStmtNode(StatementNode):
    pass


###############
# EXPRESSIONS #
###############
class ExpressionNode(AbstractNode):
    pass


class BinaryExpNode(ExpressionNode):
    pass


class UnaryExpNode(ExpressionNode):
    pass


#####################
# UNARY EXPRESSIONS #
#####################
class NotNode(UnaryExpNode):
    pass


######################
# BINARY EXPRESSIONS #
######################
class PlusNode(BinaryExpNode):
    pass


class MinusNode(BinaryExpNode):
    pass


class MultiplyNode(BinaryExpNode):
    pass


class DivideNode(BinaryExpNode):
    pass


class ModuloNode(BinaryExpNode):
    pass


class EqualsNode(BinaryExpNode):
    pass


class EqualNode(BinaryExpNode):
    pass


class NotEqualNode(BinaryExpNode):
    pass


class GreaterThanNode(BinaryExpNode):
    pass


class LessThanNode(BinaryExpNode):
    pass


class Node(BinaryExpNode):
    pass


class OrNode(BinaryExpNode):
    pass


class AndNode(BinaryExpNode):
    pass
