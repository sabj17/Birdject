class AbstractNode:

    def __init__(self):
        pass


class ProgNode(AbstractNode):
    def __init__(self, stmts):
        self.stmts = stmts


###############
# STATEMENTS #
###############
class StatementNode(AbstractNode):
    pass


class IfStmtNode(StatementNode):
    pass


class WhenStmtNode(StatementNode):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block


class ForStmtNode(StatementNode):
    def __init__(self, id, expression, block):
        self.id = id
        self.expression = expression
        self.block = block


class VarDcl(StatementNode):
    pass


class FuncDcl(StatementNode):
    def __init__(self, id, params, block):
        self.id = id
        self.params = params
        self.block = block


class ClassDcl(StatementNode):
    def __init__(self, id, body_parts):
        self.id = id
        self.body_parts = body_parts


###############
# EXPRESSIONS #
###############
class ExpressionNode(AbstractNode):
    pass


class BinaryExpNode(ExpressionNode):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        # Maybe have operand here instead of having many classes for it?


class UnaryExpNode(ExpressionNode):
    pass


# UNARY EXPRESSIONS #
class NotNode(UnaryExpNode):
    pass


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
    pass


class BlockBodyPartNode(AbstractNode):
    pass


class ReturnNode(BlockBodyPartNode):
    def __init__(self, expression):
        self.expression = expression


class BreakNode(BlockBodyPartNode):
    pass


class RunNode(BlockBodyPartNode):
    pass


###############
# CLASS STUFF #
###############
class ClassBodyPart(AbstractNode):
    def __init__(self, dcl):
        self.dcl = dcl


###################
# PARAMETER STUFF #
###################
class ParameterNode(AbstractNode):
    def __init__(self, expr):
        self.expr = expr


##############
# TERM STUFF #
##############
class TermNode(AbstractNode):
    pass


class BoolNode(TermNode):
    pass


class StringNode(TermNode):
    pass


class ValueNode(TermNode):  # Maybe have float and int node instead?
    pass


class IdNode(TermNode):
    pass


'''
Need to do
Array
Dot notation
Id operation

'''