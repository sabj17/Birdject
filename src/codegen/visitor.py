from multipledispatch import dispatch

from src.ast import ProgNode, StatementNode, ExpressionNode, BlockNode, ParameterNode, TermNode


class NodeVisitor:

    def visit(self, node):
        pass


class CodeGenVisitor(NodeVisitor):

    @dispatch(ProgNode)
    def visit(self, node):
        pass

    @dispatch(StatementNode)
    def visit(self, node):
        pass

    @dispatch(ExpressionNode)
    def visit(self, node):
        pass

    @dispatch(BlockNode)
    def visit(self, node):
        pass

    @dispatch(ParameterNode)
    def visit(self, node):
        pass

    @dispatch(TermNode)
    def visit(self, node):
        pass