from src.ast import *
from src.grammar import *
from graphviz import Digraph, nohtml
import random


class PTNode:

    def __init__(self, symbol, value, parent=None):
        self.name = symbol.name
        self.children = []
        self.value = value
        self.symbol = symbol
        self.parent = parent
        self.is_checked = False

    def add_child(self, child):
        self.children.append(child)

    def graph(self, graph, parent=None):
        id = str(hash(self))
        graph.node(id, nohtml(self.name + ": " + str(self.value)))
        if parent is not None:
            graph.edge(parent, id)

        for child in self.children:
            child.graph(graph, id)

    def accept(self, visitor):
        return visitor.visit(self)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.symbol.name) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return ""


class ParseTree:

    def __init__(self, root):
        self.root = root
        self.current_node = root
        self.is_done = False

    def add_nodes(self, nodes):
        self.current_node.children = nodes
        for node in self.current_node.children:
            node.parent = self.current_node
            if isinstance(node.symbol, Lambda):
                node.is_checked = True
        self.find_next()

    def find_next(self):

        if self.current_node is None:
            self.is_done = True
            return

        if all([n.is_checked for n in self.current_node.children]):
            self.current_node.is_checked = True
            self.current_node = self.current_node.parent
            self.find_next()
        else:
            for child in self.current_node.children:
                if child.is_checked is False:
                    self.current_node = child
                    break

    def leaf_found(self, value):
        self.current_node.value = value
        self.find_next()


    def accept(self, visitor):
        return self.root.accept(visitor)


    def graph(self):
        graph = Digraph('G', node_attr={'style': 'filled'}, graph_attr={'ratio': 'fill', 'ranksep': '1.5'})
        graph.attr(overlap='false')
        self.root.graph(graph)
        graph.save(filename='parse_tree.gv')

    def __str__(self):
        return self.root.__str__()



class BuildASTVisitor:

    def visit(self, node):
        ast_child_nodes = self.visit_children(node)

        node_name = node.name.replace('<', '').replace('>', '').replace('-', '_')  # format it to a legal function name
        method_name = 'visit_' + node_name
        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node, ast_child_nodes)
        else:
            # if there is no method for the node, pass the found nodes up the tree
            if ast_child_nodes:
                content, = ast_child_nodes
                return content



    def visit_children(self, node):
        ast_child_nodes = []
        for child in node.children:
            ast_node = child.accept(self)
            if ast_node is not None:
                ast_child_nodes.append(ast_node)
        return ast_child_nodes


    def visit_prog(self, node, ast_children):
        # <prog> -> <stmts>, $
        assert node.name == '<prog>'
        stmts, = ast_children
        prog_node = ProgNode(stmts)
        return AST(prog_node)

    def visit_stmts(self, node, ast_children):
        # <stmts> -> <stmt>, <stmts> | LAMBDA
        assert node.name == '<stmts>'
        if len(ast_children) == 2:
            stmt, stmt_list = ast_children
            return [stmt] + stmt_list
        elif len(ast_children) == 1:
            stmt, = ast_children
            return [stmt]
        else:
            return []

    def visit_class_dcl(self, node, ast_children):
        # <class-dcl> -> ID, LCURLY, <class-body>, RCURLY
        assert node.name == '<class-dcl>'
        id_node, body_parts = ast_children
        class_body = ClassBodyNode(body_parts)
        return ClassNode(id_node, class_body)

    def visit_class_body(self, node, ast_children):
        # <class-body> -> <class-body-part>, <class-body> | <class-body> -> LAMBDA
        assert node.name == '<class-body>'

        if len(ast_children) == 2:
            part, part_list = ast_children
            return [part] + part_list
        elif len(ast_children) == 1:
            part, = ast_children
            return [part]
        else:
            return []

    def visit_func_dcl(self, node, ast_children):
        # <func-dcl> -> FUNCTION, ID, LPAREN, <formal-params>, RPAREN, <block>
        assert node.name == '<func-dcl>'

        if len(ast_children) == 3:
            id_node, params, block = ast_children
            return FunctionNode(id_node, params, block)
        elif len(ast_children) == 2:
            id_node, block = ast_children
            return FunctionNode(id_node, None, block)


    def visit_var_dcl(self, node, ast_children):
        # <var-dcl> -> SET, <id-ref>, TO, <expr>, END
        assert node.name == '<var-dcl>'
        id_node, expr = ast_children
        return AssignNode(id_node, expr)


    def visit_return(self, node, ast_children):
        # <return> -> RETURN, <expr>, END
        assert node.name == '<return>'
        expr, = ast_children
        return ReturnNode(expr)

    def visit_break(self, node, ast_children):
        # <break> -> BREAK, END
        assert node.name == '<break>'
        return BreakNode()

    def visit_when_stmt(self, node, ast_children):
        # <when-stmt> -> WHEN, LPAREN, <expr>, RPAREN, <block>
        assert node.name == '<when-stmt>'

        expr, block = ast_children
        return WhenNode(expr, block)

    def visit_for_stmt(self, node, ast_children):
        # <for-stmt> -> FOREACH, <id>, IN, <expr>, <block>
        assert node.name == '<for-stmt>'

        id_node, expr, block = ast_children
        return ForNode(id_node, expr, block)

    def visit_if_stmt(self, node, ast_chilren):
        # <if-stmt> -> IF, LPAREN, <expr>, RPAREN, <block>, <else-clause>
        assert node.name == '<if-stmt>'

        if len(ast_chilren) == 3:
            expr, true_block, false_block = ast_chilren
            return IfNode(expr, true_block, false_block)
        elif len(ast_chilren) == 2:
            expr, true_block = ast_chilren
            return IfNode(expr, true_block, None)

    def visit_run(self, node, ast_children):
        # <run> -> RUN, <id-ref>, LPAREN, <actual-params>, RPAREN
        assert node.name == '<run>'
        if len(ast_children) == 2:
            id_node, param_node = ast_children
            return RunNode(id_node, param_node)
        elif len(ast_children) == 1:
            id_node, = ast_children
            return RunNode(id_node, None)


    def visit_block(self, node, ast_children):
        # <block> -> LCURLY, <block-body>, RCURLY
        assert node.name == '<block>'
        block_body_parts, = ast_children
        return BlockNode(block_body_parts)

    def visit_block_body(self, node, ast_children):
        # <block-body> -> <block-body-part>, <block-body> | LAMBDA
        assert node.name == '<block-body>'
        if len(ast_children) == 2:
            body_part, body_parts = ast_children
            return [body_part] + body_parts
        elif len(ast_children) == 1:
            body_part, = ast_children
            return [body_part]
        else:
            return []


    def visit_formal_params(self, node, ast_children):
        # <formal-params> -> ID, <multi-formal-params> | <formal-params> -> LAMBDA
        assert node.name == '<formal-params>'

        if ast_children:
            id_node, id_list = ast_children
            parameters = [id_node] + id_list
            return FormalParameterNode(parameters)
        else:
            return None


    def visit_multi_formal_params(self, node, ast_children):
        # <multi-formal-params> -> COMMA, ID, <multi-formal-params> | LAMBDA
        assert node.name == '<multi-formal-params>'
        if ast_children:
            id_node, id_list = ast_children
            return [id_node] + id_list
        else:
            return []


    def visit_actual_params(self, node, ast_children):
        # <actual-params> -> <expr>, <multi-actual-params> | LAMBDA
        assert node.name == '<actual-params>'

        if ast_children:
            expr, expr_list = ast_children
            parameters = [expr] + expr_list
            return ActualParameterNode(parameters)
        else:
            return None


    def visit_multi_actual_params(self, node, ast_children):
        # <multi-actual-params> -> COMMA, <expr>, <multi-actual-params> | LAMBDA
        assert node.name == '<multi-actual-params>'
        if ast_children:
            expr, expr_list = ast_children
            return [expr] + expr_list
        else:
            return []

    def visit_expr(self, node, ast_children):
        assert node.name == '<expr>'

        if len(ast_children) == 1:
            expr, = ast_children
            return expr
        elif len(ast_children) == 2:
            expr, binary_expr = ast_children
            binary_expr.expr1 = expr
            return binary_expr

    def visit_or(self, node, ast_children):
        # <or> -> OR, <expr> | LAMBDA
        assert node.name == '<or>'

        if ast_children:
            expr, = ast_children
            return OrNode(None, expr)


    def visit_logic_expr(self, node, ast_children):
        assert node.name == '<logic-expr>'

        if len(ast_children) == 1:
            expr, = ast_children
            return expr
        elif len(ast_children) == 2:
            expr, binary_expr = ast_children
            binary_expr.expr1 = expr
            return binary_expr

    def visit_and(self, node, ast_children):
        # <and> -> AND, <logic-expr> | LAMBDA
        assert node.name == '<and>'

        if ast_children:
            expr, = ast_children
            return AndNode(None, expr)

    def visit_compare_expr1(self, node, ast_children):
        assert node.name == '<compare-expr1>'

        if len(ast_children) == 1:
            expr, = ast_children
            return expr
        elif len(ast_children) == 2:
            expr, binary_expr = ast_children
            binary_expr.expr1 = expr
            return binary_expr

    def visit_compare_op1(self, node, ast_children):
        # <compare-op1> -> EQUALS, <compare-expr1> | NOTEQUALS, <compare-expr1> | LAMBDA
        assert node.name == '<compare-op1>'
        first_child = node.children[0].name

        if first_child == 'EQUALS':
            expr, = ast_children
            return EqualsNode(None, expr)
        elif first_child == 'NOTEQUALS':
            expr, = ast_children
            return NotEqualNode(None, expr)

    def visit_compare_expr2(self, node, ast_children):
        assert node.name == '<compare-expr2>'

        if len(ast_children) == 1:
            expr, = ast_children
            return expr
        elif len(ast_children) == 2:
            expr, binary_expr = ast_children
            binary_expr.expr1 = expr
            return binary_expr

    def visit_compare_op2(self, node, ast_children):
        # <compare-op2> -> LESS, <compare-expr2> | GREATER, <compare-expr2> | LAMBDA
        assert node.name == '<compare-op2>'
        first_child = node.children[0].name

        if first_child == 'LESS':
            expr, = ast_children
            return LessThanNode(None, expr)
        elif first_child == 'GREATER':
            expr, = ast_children
            return GreaterThanNode(None, expr)

    def visit_arith_expr1(self, node, ast_children):
        assert node.name == '<arith-expr1>'

        if len(ast_children) == 1:
            expr, = ast_children
            return expr
        elif len(ast_children) == 2:
            expr, binary_expr = ast_children
            binary_expr.expr1 = expr
            return binary_expr

    def visit_arith_op1(self, node, ast_children):
        # <arith-op1> -> PLUS, <arith-expr1> | MINUS, <arith-expr1> | LAMBDA
        assert node.name == '<arith-op1>'
        first_child = node.children[0].name

        if first_child == 'PLUS':
            expr, = ast_children
            return PlusNode(None, expr)
        elif first_child == 'MINUS':
            expr, = ast_children
            return MinusNode(None, expr)

    def visit_arith_expr2(self, node, ast_children):
        # <arith-expr2> -> <arith-expr3>, <arith-op2>
        assert node.name == '<arith-expr2>'

        if len(ast_children) == 1:
            expr, = ast_children
            return expr
        elif len(ast_children) == 2:
            expr, binary_expr = ast_children
            binary_expr.expr1 = expr
            return binary_expr

    def visit_arith_op2(self, node, ast_children):
        # <arith-op2> -> MULT, <arith-expr2> | DIVIDE, <arith-expr2> | MODULO, <arith-expr2> | LAMBDA
        assert node.name == '<arith-op2>'
        first_child = node.children[0].name

        if first_child == 'MULT':
            expr, = ast_children
            return MultiplyNode(None, expr)
        elif first_child == 'DIVIDE':
            expr, = ast_children
            return DivideNode(None, expr)
        elif first_child == 'MODULO':
            expr, = ast_children
            return ModuloNode(None, expr)


    def visit_arith_expr3(self, node, ast_children):
        # <arith-expr3> -> <term> | LPAREN, <expr>, RPAREN | MINUS, <arith-expr3> | NOT, <arith-expr3>
        assert node.name == '<arith-expr3>'

        first_child = node.children[0].name  # first child of the parse tree node
        expr, = ast_children

        if first_child == '<term>':
            return expr
        elif first_child == 'LPAREN':
            return ParenthesesNode(expr)
        elif first_child == 'MINUS':
            return NegativeNode(expr)
        elif first_child == 'NOT':
            return NotNode(expr)

    def visit_id_operation(self, node, ast_children):
        # <id-operation> -> <id>, <id-operator>
        assert node.name == '<id-operation>'

        if len(ast_children) == 2:
            id_node, id_op = ast_children
            if isinstance(id_op, DotNode):
                id_op.ids.insert(0, id_node)
                return id_op
            elif isinstance(id_op, IdNode):
                return DotNode([id_node, id_op])
            elif isinstance(id_op, ActualParameterNode):
                return NewObjectNode(id_node, id_op)

        elif len(ast_children) == 1:
            id_node, = ast_children
            return id_node

    def visit_id_ref(self, node, ast_children):
        # <id-ref> -> <id>, <dot-ref>
        assert node.name == '<id-ref>'
        if len(ast_children) == 2:
            id_node, dot_node = ast_children
            dot_node.ids.insert(0, id_node)
            return dot_node

        elif len(ast_children) == 1:
            id_node, = ast_children
            return id_node

    def visit_dot_ref(self, node, ast_children):
        # <dot-ref> -> DOT, <id>, <dot-ref> | LAMBDA
        assert node.name == '<dot-ref>'
        if len(ast_children) == 2:
            id_node, other_node = ast_children
            if isinstance(other_node, DotNode):
                other_node.ids.insert(0, id_node)
                return other_node
            elif isinstance(other_node, IdNode):
                return DotNode([id_node, other_node])

        elif len(ast_children) == 1:
            id_node, = ast_children
            return DotNode([id_node])

    def visit_id(self, node, ast_children):
        # <id> -> ID, <array-subscript>
        assert node.name == '<id>'
        if len(ast_children) == 2:
            id_node, int_node = ast_children
            return ArrayRefNode(id_node, int_node)
        elif len(ast_children) == 1:
            id_node, = ast_children
            return id_node

    def visit_ID(self, node, ast_children):
        assert not ast_children
        return IdNode(node.value)

    def visit_INTEGER(self, node, ast_children):
        assert not ast_children
        return IntegerNode(node.value)

    def visit_FLOAT(self, node, ast_children):
        assert not ast_children
        return FloatNode(node.value)

    def visit_BOOL(self, node, ast_children):
        assert not ast_children
        return BoolNode(node.value)

    def visit_STRING(self, node, ast_children):
        assert not ast_children
        return StringNode(node.value)
