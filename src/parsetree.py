from src.grammar import *
from graphviz import Digraph, nohtml
import random
from src.ast import *

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
        id = str(random.randint(1, 10000000))
        graph.node(id, nohtml(self.name + ": " + str(self.value)))
        if parent is not None:
            graph.edge(parent, id)

        for child in self.children:
            child.graph(graph, id)

    def accept(self, visitor):
        visitor.visit(self)

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

    def to_AST(self):
        visitor = BuildASTVisitor()
        self.root.accept(visitor)
        visitor.tree.graph()

    def graph(self):
        graph = Digraph('G', node_attr={'style': 'filled'}, graph_attr={'ratio': 'fill', 'ranksep': '1.5'})
        graph.attr(overlap='false')
        self.root.graph(graph)
        graph.save(filename='parse_tree.gv')

    def __str__(self):
        return self.root.__str__()


class BuildASTVisitor:

    def __init__(self):
        self.tree = None

    def visit(self, node):
        prog_node = self.visit_PROG(node)
        self.tree = AST(prog_node)

    def visit_PROG(self, node):
        stmt_list = self.visit_STMTS(node.children[0])
        return ProgNode(stmt_list)

    def visit_STMTS(self, node):
        # <stmts> -> <stmt> <stmts> | LAMBDA
        stmt_list = []

        if isinstance(node.children[0].symbol, Lambda):
            return stmt_list

        stmt = self.visit_STMT(node.children[0])
        stmts = self.visit_STMTS(node.children[1])

        if stmt:
            stmt_list.append(stmt)
        stmt_list.extend(stmts)

        return stmt_list

    def visit_STMT(self, node):
        options = {'<var-dcl>': self.visit_VAR_DCL,
                   '<class-dcl>': self.visit_CLASS_DCL,
                   '<for-stmt>': self.visit_FOR_STMT,
                   '<if-stmt>': self.visit_IF_STMT,
                   '<func-dcl>': self.visit_FUNC_DCL,
                   '<run>': self.visit_RUN,
                   '<when-stmt>': self.visit_WHEN_STMT,
                   }
        # <stmt> -> <when-stmt>
        # <stmt> -> <for-stmt>
        # <stmt> -> <if-stmt>
        # <stmt> -> <run>, END
        # <stmt> -> <var-dcl>
        # <stmt> -> <func-dcl>
        # <stmt> -> <class-dcl>
        child = node.children[0]
        if child.name in options:
            visit_func = options[child.name]
            return visit_func(child)
        return None

    def visit_VAR_DCL(self, node):
        # <var-dcl> -> SET <id-ref> TO <expr> END
        id_node = self.visit_ID_REF(node.children[1])
        expression_node = self.visit_EXPR(node.children[3])

        return AssignNode(id_node, expression_node)

    def visit_RUN(self, node):
        # <run> -> RUN, <id-ref>, LPAREN, <params>, RPAREN
        id = self.visit_ID_REF(node.children[1])
        params = self.visit_PARAMS(node.children[3])

        return RunNode(id, params)

    def visit_FUNC_DCL(self, node):
        # <func-dcl> -> FUNCTION, ID, LPAREN, <params>, RPAREN, <block>
        id = self.visit_ID(node.children[1])
        params = self.visit_PARAMS(node.children[3])
        block = self.visit_BLOCK(node.children[-1])

        return FunctionNode(id, params, block)

    def visit_CLASS_DCL(self, node):
        # <class-dcl> -> ID, LCURLY, <class-body>, RCURLY
        id = self.visit_ID(node.children[0])
        body = self.visit_CLASS_BODY(node.children[2])
        body = ClassBodyNode(body)

        return ClassNode(id, body)

    def visit_CLASS_BODY(self, node):
        # <class-body> -> <class-body-part>, <class-body>
        body_parts = []

        if isinstance(node.children[0].symbol, Lambda):
            return body_parts

        body_part = self.visit_CLASS_BODY_PART(node.children[0])
        body = self.visit_CLASS_BODY(node.children[1])

        body_parts.append(body_part)
        body_parts.extend(body)

        return body_parts

    def visit_CLASS_BODY_PART(self, node):
        # <class-body-part> -> <var-dcl> | <func-dcl> | <class-dcl>
        options = {'<var-dcl>': self.visit_VAR_DCL,
                   '<class-dcl>': self.visit_CLASS_DCL,
                   '<func-dcl>': self.visit_FUNC_DCL
                   }

        child = node.children[0]
        visit_func = options[child.name]
        return visit_func(child)

    def visit_WHEN_STMT(self, node):
        # <when-stmt> -> WHEN, LPAREN, <expr>, RPAREN, <block>
        expr = self.visit_EXPR(node.children[2])
        block = self.visit_BLOCK(node.children[4])

        return WhenNode(expr, block)

    def visit_FOR_STMT(self, node):
        # <for-stmt> -> FOREACH, <id>, IN, <expr>, <block>
        id = self.visit_ARRAY_REF(node.children[1])
        expr = self.visit_EXPR(node.children[3])
        block = self.visit_BLOCK(node.children[5])

        return ForNode(id, expr, block)

    def visit_IF_STMT(self, node):
        # <if-stmt> -> IF, LPAREN, <expr>, RPAREN, <block>, <else-clause>
        expr = self.visit_EXPR(node.children[2])
        block_true = self.visit_BLOCK(node.children[4])
        block_flase = self.visit_ELSE_CLAUSE(node.children[5])

        return IfNode(expr, block_true, block_flase)

    def visit_ELSE_CLAUSE(self, node):
        # <else-clause> -> ELSE, <else> | LAMBDA

        if isinstance(node.children[0].symbol, Lambda):
            return None

        return self.visit_ELSE(node.children[1])

    def visit_ELSE(self, node):
        # <else> -> <block> | <if-stmt>
        child = node.children[0]
        if child.name == '<block>':
            return self.visit_BLOCK(child)
        if child.name == '<if-stmt>':
            return self.visit_IF_STMT(child)

    def visit_BLOCK(self, node):
        # <block> -> LCURLY, <block-body>, RCURLY

        body = self.visit_BLOCK_BODY(node.children[1])
        return BlockNode(body)

    def visit_BLOCK_BODY(self, node):
        # <block-body> -> <block-body-part> <block-body> | LAMBDA
        body_parts = []

        if isinstance(node.children[0].symbol, Lambda):
            return body_parts

        body_part = self.visit_BLOCK_BODY_PART(node.children[0])
        block_body = self.visit_BLOCK_BODY(node.children[1])

        body_parts.append(body_part)
        body_parts.extend(block_body)

        return body_parts

    def visit_BLOCK_BODY_PART(self, node):
        # <block-body-part> -> <for-stmt> | <if-stmt> | <run>, END | <return> | <var-dcl> | <break>
        options = {'<for-stmt>': self.visit_FOR_STMT,
                   '<if-stmt>': self.visit_IF_STMT,
                   '<run>': self.visit_RUN,
                   '<return>': self.visit_RETURN,
                   '<var-dc>': self.visit_VAR_DCL,
                   '<break>': self.visit_BREAK}
        child = node.children[0]
        visit_func = options[child.name]
        return visit_func(child)

    def visit_RETURN(self, node):
        # <return> -> RETURN <expr> END
        expr = self.visit_EXPR(node.children[1])
        return ReturnNode(expr)

    def visit_BREAK(self, node):
        return BreakNode()

    def visit_PARAMS(self, node):
        # <params> -> <expr> <multi-params>
        # <params> -> LAMBDA
        first_child = node.children[0]

        if not isinstance(first_child.symbol, Lambda):
            expr_list = []
            first_expr = self.visit_EXPR(first_child)
            expr_list.append(first_expr)
            multi_params = self.visit_MULTI_PARAMS(node.children[1])
            expr_list.extend(multi_params)

            return ParameterNode(expr_list)

        return None

    def visit_MULTI_PARAMS(self, node):
        # <multi-params> -> COMMA <expr> <multi-params>
        # <multi-params> -> LAMBDA
        expr_list = []
        first_child = node.children[0]
        if not isinstance(first_child.symbol, Lambda):
            expr = self.visit_EXPR(node.children[1])
            expr_list.append(expr)
            multi_params = self.visit_MULTI_PARAMS(node.children[2])
            expr_list.extend(multi_params)

        return expr_list

    def visit_ID_REF(self, node):
        # <id-ref> -> <id> <dot-ref>
        first_id = self.visit_ARRAY_REF(node.children[0])  # <id>
        dot_ref_child = node.children[1].children[0]
        if not isinstance(dot_ref_child.symbol, Lambda):  # if <dot-ref> does not derive lambda
            id_nodes = []
            other_ids = self.visit_DOT_REF(node.children[1])  # <dot-ref>
            id_nodes.append(first_id)
            id_nodes.extend(other_ids)
            return DotNode(id_nodes)

        else:
            return first_id

    def visit_DOT_REF(self, node):
        # <dot-ref> -> DOT <id> <dot-ref>
        id_list = []

        if isinstance(node.children[0].symbol, Lambda):
            return id_list

        id = self.visit_ARRAY_REF(node.children[1])
        dot_ref = self.visit_DOT_REF(node.children[2])

        id_list.append(id)
        id_list.extend(dot_ref)

        return id_list

    def visit_ARRAY_REF(self, node):
        # <id> -> ID <array-subscript>
        id_node = self.visit_ID(node.children[0])  # ID

        # <array-subscript> -> LSQUARE, INTEGER, RSQUARE | LAMBDA
        array_ss_child = node.children[1].children[0]
        if not isinstance(array_ss_child.symbol, Lambda):  # if <array-script> does not derive lambda
            integer_node = self.visit_INT(node.children[1].children[1])  #  visit second production for <array-subscript> -> LSQUARE INTEGER RSQUARE
            return ArrayRefNode(id_node, integer_node)

        return id_node

    def visit_ID(self, node):
        return IdNode(node.value)

    def visit_EXPR(self, node):
        # <expr> -> <logic-expr> <or>
        expr_node = self.visit_LOGIC_EXPR(node.children[0])

        or_children = node.children[1].children  # <or> -> OR <expr> | LAMBDA
        if not isinstance(or_children[0].symbol, Lambda):  # if <or> does not derive lambda
            left_operant = expr_node
            right_operant = self.visit_EXPR(or_children[1])
            return OrNode(left_operant, right_operant)

        return expr_node

    def visit_LOGIC_EXPR(self, node):
        # <logic-expr> -> <compare-expr1>, <and>
        expr_node = self.visit_COMPARE_EXPR_1(node.children[0])

        and_children = node.children[1].children  # <and> -> AND <logic-expr> | LAMBDA
        if not isinstance(and_children[0].symbol, Lambda):  # if <and> does not derive lambda
            left_operant = expr_node
            right_operant = self.visit_LOGIC_EXPR(and_children[1])
            return AndNode(left_operant, right_operant)

        return expr_node

    def visit_COMPARE_EXPR_1(self, node):
        # <compare-expr1> -> <compare-expr2>, <compare-op1>
        expr_node = self.visit_COMPARE_EXPR_2(node.children[0])

        comp_op_children = node.children[1].children  # <compare-op1> -> EQUALS <compare-expr1> | NOTEQUALS <compare-expr1> | LAMBDA
        if not isinstance(comp_op_children[0].symbol, Lambda):  # if <compare-op1> does not derive lambda
            left_operant = expr_node
            right_operant = self.visit_COMPARE_EXPR_1(comp_op_children[1])

            if comp_op_children[0].name == 'EQUALS':
                return EqualsNode(left_operant, right_operant)
            elif comp_op_children[0].name == 'NOTEQUALS':
                return NotEqualNode(left_operant, right_operant)

        return expr_node

    def visit_COMPARE_EXPR_2(self, node):
        # <compare-expr2> -> <arith-expr1>, <compare-op2>
        expr_node = self.visit_ARITH_EXPR_1(node.children[0])

        comp_op2_children = node.children[1].children  # <compare-op2> -> LESS <compare-expr2> | GREATER <compare-expr2> | LAMBDA

        if not isinstance(comp_op2_children[0].symbol, Lambda):  # if <compare-op2> does not derive lambda
            left_operant = expr_node
            right_operant = self.visit_COMPARE_EXPR_2(comp_op2_children[1])

            if comp_op2_children[0].name == 'LESS':
                return LessThanNode(left_operant, right_operant)
            elif comp_op2_children[0].name == 'GREATER':
                return GreaterThanNode(left_operant, right_operant)

        return expr_node

    def visit_ARITH_EXPR_1(self, node):
        # <arith-expr1> -> <arith-expr2>, <arith-op1>
        expr_node = self.visit_ARITH_EXPR_2(node.children[0])

        arith_op1_children = node.children[1].children  # <arith-op1> -> PLUS <arith-expr1> | MINUS <arith-expr1> | LAMBDA

        if not isinstance(arith_op1_children[0].symbol, Lambda):  # if <arith-op1> does not derive lambda
            left_operant = expr_node
            right_operant = self.visit_ARITH_EXPR_1(arith_op1_children[1])

            if arith_op1_children[0].name == 'PLUS':
                return PlusNode(left_operant, right_operant)
            elif arith_op1_children[0].name == 'MINUS':
                return MinusNode(left_operant, right_operant)

        return expr_node

    def visit_ARITH_EXPR_2(self, node):
        # <arith-expr2> -> <arith-expr3>, <arith-op2>
        expr_node = self.visit_ARITH_EXPR_3(node.children[0])

        arith_op2_children = node.children[1].children  # <arith-op2> -> MULT <arith-expr2> | DIVIDE <arith-expr2> | MODULO <arith-expr2> | LAMBDA

        if not isinstance(arith_op2_children[0].symbol, Lambda):  # if <arith-op2> does not derive lambda
            left_operant = expr_node
            right_operant = self.visit_ARITH_EXPR_2(arith_op2_children[1])

            if arith_op2_children[0].name == 'MULT':
                return MultiplyNode(left_operant, right_operant)
            elif arith_op2_children[0].name == 'DIVIDE':
                return DivideNode(left_operant, right_operant)
            elif arith_op2_children[0].name == 'MODULO':
                return ModuloNode(left_operant, right_operant)

        return expr_node

    def visit_ARITH_EXPR_3(self, node):
        # <arith-expr3> -> <term> | LPAREN <expr> RPAREN | MINUS <arith-expr3> | NOT <arith-expr3>

        first_child = node.children[0]
        if first_child.name == '<term>':
            return self.visit_TERM(first_child)
        elif first_child.name == 'LPAREN':
            in_paren = self.visit_EXPR(node.children[1])
            return ParenthesesNode(in_paren)
        elif first_child.name == 'MINUS':
            expr_node = self.visit_ARITH_EXPR_3(node.children[1])
            return NegativeNode(expr_node)
        elif first_child.name == 'NOT':
            expr_node = self.visit_ARITH_EXPR_3(node.children[1])
            return NotNode(expr_node)

    def visit_TERM(self, node):
        # <term> -> <id-operation> | <boolean> | <val> | <string> | <run>
        child = node.children[0]
        if child.name == '<id-operation>':
            return self.visit_ID_OP(child)
        elif child.name == '<boolean>':
            return self.visit_BOOL(child.children[0])
        elif child.name == '<val>':
            return self.visit_VAL(child)
        elif child.name == '<string>':
            return self.visit_STR(child.children[0])
        elif child.name == '<run>':
            return self.visit_RUN(child)

    def visit_ID_OP(self, node):
        # <id-operation> -> <id> <id-operator>
        # <id-operator> -> <dot-ref>
        # <id-operator> -> LPAREN, <params>, RPAREN

        id = self.visit_ARRAY_REF(node.children[0])
        id_operator_children = node.children[1].children

        if id_operator_children[0] == '<dot-ref>':
            id_list = []
            id_list.append(id)
            ids = self.visit_DOT_REF(id_operator_children[0])
            id_list.extend(ids)
            return DotNode(id_list)

        elif id_operator_children[0] == 'LPAREN':
            param_node = self.visit_PARAMS(id_operator_children[1])
            return NewObjectNode(param_node)

        return id

    def visit_VAL(self, node):
        child = node.children[0]

        if child.name == 'FLOAT':
            return self.visit_FLOAT(child)
        elif child.name == 'INTEGER':
            return self.visit_INT(child)

    def visit_INT(self, node):
        return IntegerNode(node.value)

    def visit_BOOL(self, node):
        return BoolNode(node.value)

    def visit_STR(self, node):
        return StringNode(node.value)

    def visit_FLOAT(self, node):
        return FloatNode(node.value)
