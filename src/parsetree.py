from ast import IdNode, ArrayRefNode, AST, ProgNode, AssignNode, RunNode, FunctionNode, ClassBodyNode, ClassNode, \
    WhenNode, ForNode, IfNode, BlockNode, ReturnNode, BreakNode, ActualParameterNode, FormalParameterNode, DotNode, \
    OrNode, AndNode, EqualsNode, NotEqualNode, LessThanNode, GreaterThanNode, PlusNode, MinusNode, MultiplyNode, \
    DivideNode, ModuloNode, ParenthesesNode, NegativeNode, NotNode, NewObjectNode, IntegerNode, BoolNode, StringNode, \
    FloatNode
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
        id = str(random.randint(1, 10000000))
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

    def to_AST(self):
        visitor = BuildASTVisitor()
        ast = self.root.accept(visitor)
        return ast

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
        prog_node = self.visit_PROG(node)  # Call visit_PROG to get the root node
        return AST(prog_node)  # Make AST from root node

    def visit_PROG(self, node):
        # <prog> -> <stmts> $
        stmt_list = self.visit_STMTS(node.children[0])  # call visit_STMTS to get a list of statements
        return ProgNode(stmt_list)  # use the statement list to make a prog node

    def visit_STMTS(self, node):
        # <stmts> -> <stmt> <stmts> | LAMBDA
        stmt_list = []

        # if <stmts> derive lambda return an empty list of statements
        if isinstance(node.children[0].symbol, Lambda):
            return stmt_list

        # visit stmt to get the statement, visit stmts to get a list of the rest of the statements
        stmt = self.visit_STMT(node.children[0])
        stmts = self.visit_STMTS(node.children[1])

        stmt_list.append(stmt)
        stmt_list.extend(stmts)  # append each of the elements in stmts

        return stmt_list  # returns a list of statements

    def visit_STMT(self, node):
        # <stmt> -> <when-stmt> | <for-stmt> | <if-stmt> | <run>, END | <var-dcl> | <func-dcl> | <class-dcl>
        options = {'<var-dcl>': self.visit_VAR_DCL,
                   '<class-dcl>': self.visit_CLASS_DCL,
                   '<for-stmt>': self.visit_FOR_STMT,
                   '<if-stmt>': self.visit_IF_STMT,
                   '<func-dcl>': self.visit_FUNC_DCL,
                   '<run>': self.visit_RUN,
                   '<when-stmt>': self.visit_WHEN_STMT,
                   }
        # based on what node we are at, call the appropriate function from 'options'
        child = node.children[0]
        visit_func = options[child.name]
        return visit_func(child)  # return the statement

    def visit_VAR_DCL(self, node):
        # <var-dcl> -> SET <id-ref> TO <expr> END
        id_node = self.visit_ID_REF(node.children[1])  # Call visit_ID_REF to get the id for the var dcl
        expression_node = self.visit_EXPR(node.children[3])  # Call visit_EXPR to get the expression

        return AssignNode(id_node, expression_node)  # Make an AssignNode and return it

    def visit_RUN(self, node):
        # <run> -> RUN, <id-ref>, LPAREN, <params>, RPAREN
        id = self.visit_ID_REF(node.children[1])  # visit_ID_REF to get the id
        params = self.visit_ACTUAL_PARAMS(node.children[3])  # visit params to get the param node

        return RunNode(id, params)  # Make a RunNode and return it

    def visit_FUNC_DCL(self, node):
        # <func-dcl> -> FUNCTION, ID, LPAREN, <params>, RPAREN, <block>
        id = self.visit_ID(node.children[1])  # visit_ID to get the IdNode
        params = self.visit_FORMAL_PARAMS(node.children[3])  # visit_PARAMS to get the ParamNode
        block = self.visit_BLOCK(node.children[-1])  # visit_BLOCK to get the BlockNode

        return FunctionNode(id, params, block)  # Make a FunctionNode and return it

    def visit_CLASS_DCL(self, node):
        # <class-dcl> -> ID, LCURLY, <class-body>, RCURLY
        id = self.visit_ID(node.children[0])  # visit_ID to get the IdNode
        body = self.visit_CLASS_BODY(node.children[2])  # visit_CLASS_BODY to get a list of body parts
        body = ClassBodyNode(body)  # use the body parts to make a ClassBodyNode

        return ClassNode(id, body)  # Make the ClassNode and return it

    def visit_CLASS_BODY(self, node):
        # <class-body> -> <class-body-part>, <class-body> | LAMBDA
        body_parts = []

        # if <class-body> derives lambda return and empty list of body parts
        if isinstance(node.children[0].symbol, Lambda):
            return body_parts

        body_part = self.visit_CLASS_BODY_PART(node.children[0])  # get the first body part
        body = self.visit_CLASS_BODY(node.children[1])  # get the rest of the body parts

        # appends the body parts to 'body_parts'
        body_parts.append(body_part)
        body_parts.extend(body)

        return body_parts  # return the list of body parts

    def visit_CLASS_BODY_PART(self, node):
        # <class-body-part> -> <var-dcl> | <func-dcl> | <class-dcl>
        options = {'<var-dcl>': self.visit_VAR_DCL,
                   '<class-dcl>': self.visit_CLASS_DCL,
                   '<func-dcl>': self.visit_FUNC_DCL
                   }
        # visit on of these options depending on the input node

        child = node.children[0]
        visit_func = options[child.name]
        return visit_func(child)

    def visit_WHEN_STMT(self, node):
        # <when-stmt> -> WHEN, LPAREN, <expr>, RPAREN, <block>
        expr = self.visit_EXPR(node.children[2])  # visit_EXPR to get the expression for the when statement
        block = self.visit_BLOCK(node.children[4])  # visit_BLOCK to get the block for the when statement

        return WhenNode(expr, block)  # Create a WhenNode and return it

    def visit_FOR_STMT(self, node):
        # <for-stmt> -> FOREACH, <id>, IN, <expr>, <block>
        id = self.visit_ARRAY_REF(node.children[1])  # get the id from visit_ARRAY_REF
        expr = self.visit_EXPR(node.children[3])  # visit_EXPR to get the expression
        block = self.visit_BLOCK(node.children[5])  # visit_BLOCK to get the block belonging to the for-stmt

        return ForNode(id, expr, block)  # create a ForNode and return it

    def visit_IF_STMT(self, node):
        # <if-stmt> -> IF, LPAREN, <expr>, RPAREN, <block>, <else-clause>
        expr = self.visit_EXPR(node.children[2])  # visit_EXPR to get the expression
        block_true = self.visit_BLOCK(
            node.children[4])  # visit_BLOCK to get the block which will execute if the expr is true
        block_flase = self.visit_ELSE_CLAUSE(
            node.children[5])  # visit_ELSE_CLAUSE block/statement that will execute if expr is false

        return IfNode(expr, block_true, block_flase)  # Create an IfNode and return it

    def visit_ELSE_CLAUSE(self, node):
        # <else-clause> -> ELSE, <else> | LAMBDA

        # return None if there is no else (<else-clause> derives lambda)
        if isinstance(node.children[0].symbol, Lambda):
            return None

        return self.visit_ELSE(node.children[1])  # return visit_ELSE that finds what is in the else statement

    def visit_ELSE(self, node):
        # <else> -> <block> | <if-stmt>
        child = node.children[0]

        if child.name == '<block>':  # if the node is a block, return visit_BLOCK
            return self.visit_BLOCK(child)
        if child.name == '<if-stmt>':  # if the node is and if stmt, return visit_IF_STMT
            return self.visit_IF_STMT(child)

    def visit_BLOCK(self, node):
        # <block> -> LCURLY, <block-body>, RCURLY

        body = self.visit_BLOCK_BODY(node.children[1])  # visit_BLOCK_BODY to get the list of body parts
        return BlockNode(body)  # Create a BlockNode and return it

    def visit_BLOCK_BODY(self, node):
        # <block-body> -> <block-body-part> <block-body> | LAMBDA
        body_parts = []

        # if block-body is empty return an empty list
        if isinstance(node.children[0].symbol, Lambda):
            return body_parts

        body_part = self.visit_BLOCK_BODY_PART(node.children[0])  # get a body part
        block_body = self.visit_BLOCK_BODY(node.children[1])  # get the rest of the body parts

        # append all body parts to the list
        body_parts.append(body_part)
        body_parts.extend(block_body)

        return body_parts  # return the list of body parts

    def visit_BLOCK_BODY_PART(self, node):
        # <block-body-part> -> <for-stmt> | <if-stmt> | <run>, END | <return> | <var-dcl> | <break>
        options = {'<for-stmt>': self.visit_FOR_STMT,
                   '<if-stmt>': self.visit_IF_STMT,
                   '<run>': self.visit_RUN,
                   '<return>': self.visit_RETURN,
                   '<var-dcl>': self.visit_VAR_DCL,
                   '<break>': self.visit_BREAK}
        # call visit for one of these based on the body part

        child = node.children[0]
        visit_func = options[child.name]
        return visit_func(child)

    def visit_RETURN(self, node):
        # <return> -> RETURN <expr> END
        expr = self.visit_EXPR(node.children[1])  # visit_EXPR to get the expression that will be returned
        return ReturnNode(expr)  # Create the ReturnNode and return it

    def visit_BREAK(self, node):
        return BreakNode()  # return a BreakNode

    def visit_ACTUAL_PARAMS(self, node):
        # <actual-params> -> <expr> <multi-actual-params> | <params> -> LAMBDA
        first_child = node.children[0]

        if not isinstance(first_child.symbol, Lambda):
            expr_list = []
            first_expr = self.visit_EXPR(first_child)  # get the expression
            multi_params = self.visit_MULTI_ACTUAL_PARAMS(node.children[1])  # get the rest of the expressions

            # append all expressions to a list
            expr_list.append(first_expr)
            expr_list.extend(multi_params)

            return ActualParameterNode(expr_list)  # Create a ActualParameterNode using the list of expressions and return it

        return None  # return None if <actual-params> derives lambda

    def visit_MULTI_ACTUAL_PARAMS(self, node):
        # <multi-actual-params> -> COMMA ID <multi-actual-params> | LAMBDA
        expr_list = []
        first_child = node.children[0]
        if not isinstance(first_child.symbol, Lambda):
            expr = self.visit_EXPR(node.children[1])  # get the expression
            multi_params = self.visit_MULTI_ACTUAL_PARAMS(node.children[2])  # get the rest of the expressions

            # append all expression to a list
            expr_list.append(expr)
            expr_list.extend(multi_params)

        # if <multi-actual-params> derives empty return and empty list of expressions
        # else return a list of expressions
        return expr_list

    def visit_FORMAL_PARAMS(self, node):
        # <formal-params> -> ID <multi-formal-params> | <formal-params> -> LAMBDA
        first_child = node.children[0]

        if not isinstance(first_child.symbol, Lambda):
            id_list = []
            first_id = self.visit_ID(first_child)  # get the id
            multi_params = self.visit_MULTI_FORMAL_PARAMS(node.children[1])  # get the rest of the ids

            # append all expressions to a list
            id_list.append(first_id)
            id_list.extend(multi_params)

            return FormalParameterNode(id_list)  # Create a FormalParameterNode using the list of ids and return it

        return None  # return None if <formal-params> derives lambda

    def visit_MULTI_FORMAL_PARAMS(self, node):
        # <multi-formal-params> -> COMMA ID <multi-formal-params> | LAMBDA
        id_list = []
        first_child = node.children[0]
        if not isinstance(first_child.symbol, Lambda):
            id = self.visit_ID(node.children[1])  # get the id
            multi_params = self.visit_MULTI_FORMAL_PARAMS(node.children[2])  # get the rest of the ids

            # append all expression to a list
            id_list.append(id)
            id_list.extend(multi_params)

        # if <multi-formal-params> derives empty return and empty list of ids
        # else return a list of ids
        return id_list

    def visit_ID_REF(self, node):
        # <id-ref> -> <id> <dot-ref>
        first_id = self.visit_ARRAY_REF(node.children[0])  # <id>
        dot_ref_child = node.children[1].children[0]

        # if dot-ref derives lambda return the IdNode from visit_ARRAY_REF
        # else return a DotNode that has a list of IdNodes
        if not isinstance(dot_ref_child.symbol, Lambda):
            id_nodes = []
            other_ids = self.visit_DOT_REF(node.children[1])
            id_nodes.append(first_id)
            id_nodes.extend(other_ids)
            return DotNode(id_nodes)

        else:
            return first_id

    def visit_DOT_REF(self, node):
        # <dot-ref> -> DOT <id> <dot-ref> | LAMBDA
        id_list = []

        # return an empty list if dot-ref derives empty
        if isinstance(node.children[0].symbol, Lambda):
            return id_list

        id = self.visit_ARRAY_REF(node.children[1])  # visit_ARRAY_REF to get the first IdNode
        dot_ref = self.visit_DOT_REF(node.children[2])  # visit_DOT_REF to get the rest of the IdNodes

        # append all the IdNodes
        id_list.append(id)
        id_list.extend(dot_ref)

        return id_list  # return a list of IdNodes

    def visit_ARRAY_REF(self, node):
        # <id> -> ID <array-subscript>
        id_node = self.visit_ID(node.children[0])  # ID

        # <array-subscript> -> LSQUARE, INTEGER, RSQUARE | LAMBDA
        # if <array-subscript> does not derive lambda, return ArrayRefNode else just return the IdNode
        array_ss_child = node.children[1].children[0]
        if not isinstance(array_ss_child.symbol, Lambda):
            integer_node = self.visit_INT(node.children[1].children[1])
            return ArrayRefNode(id_node, integer_node)

        return id_node

    def visit_ID(self, node):
        return IdNode(node.value)  # return the IdNode

    def visit_EXPR(self, node):
        # <expr> -> <logic-expr> <or>
        expr_node = self.visit_LOGIC_EXPR(node.children[0])

        or_children = node.children[1].children
        # <or> -> OR <expr> | LAMBDA
        # if <or> does not derive lambda return OrNode else just return the expression
        if not isinstance(or_children[0].symbol, Lambda):
            left_operant = expr_node  # use the expr_node as the left operant
            right_operant = self.visit_EXPR(or_children[1])  # visit_EXPR to find the right operant
            return OrNode(left_operant, right_operant)

        return expr_node

    def visit_LOGIC_EXPR(self, node):
        # <logic-expr> -> <compare-expr1>, <and>
        expr_node = self.visit_COMPARE_EXPR_1(node.children[0])

        and_children = node.children[1].children
        # <and> -> AND <logic-expr> | LAMBDA
        # if <and> does not derive lambda return an AndNode else just return the expression
        if not isinstance(and_children[0].symbol, Lambda):
            left_operant = expr_node  # use the expr_node as the left operant
            right_operant = self.visit_LOGIC_EXPR(and_children[1])  # visit_LOGIC_EXPR to find the right operant
            return AndNode(left_operant, right_operant)

        return expr_node

    def visit_COMPARE_EXPR_1(self, node):
        # <compare-expr1> -> <compare-expr2>, <compare-op1>
        expr_node = self.visit_COMPARE_EXPR_2(node.children[0])

        comp_op_children = node.children[1].children
        # <compare-op1> -> EQUALS <compare-expr1> | NOTEQUALS <compare-expr1> | LAMBDA
        # if <compare-op1> does not derive lambda return either a EqualsNode or a NotEqualNode else just return the expression
        if not isinstance(comp_op_children[0].symbol, Lambda):
            left_operant = expr_node  # use the expr_node as the left operant
            right_operant = self.visit_COMPARE_EXPR_1(
                comp_op_children[1])  # visit_COMPARE_EXPR_1 to find the right operant

            if comp_op_children[0].name == 'EQUALS':
                return EqualsNode(left_operant, right_operant)
            elif comp_op_children[0].name == 'NOTEQUALS':
                return NotEqualNode(left_operant, right_operant)

        return expr_node

    def visit_COMPARE_EXPR_2(self, node):
        # <compare-expr2> -> <arith-expr1>, <compare-op2>
        expr_node = self.visit_ARITH_EXPR_1(node.children[0])

        comp_op2_children = node.children[
            1].children  # <compare-op2> -> LESS <compare-expr2> | GREATER <compare-expr2> | LAMBDA
        # if <compare-op2> does not derive lambda return either a LessThanNode or a GreaterThanNode
        # else just return the expression
        if not isinstance(comp_op2_children[0].symbol, Lambda):
            left_operant = expr_node  # use the expr_node as the left operant
            right_operant = self.visit_COMPARE_EXPR_2(
                comp_op2_children[1])  # visit_COMPARE_EXPR_2 to find the right operant

            if comp_op2_children[0].name == 'LESS':
                return LessThanNode(left_operant, right_operant)
            elif comp_op2_children[0].name == 'GREATER':
                return GreaterThanNode(left_operant, right_operant)

        return expr_node

    def visit_ARITH_EXPR_1(self, node):
        # <arith-expr1> -> <arith-expr2>, <arith-op1>
        expr_node = self.visit_ARITH_EXPR_2(node.children[0])

        arith_op1_children = node.children[1].children
        # <arith-op1> -> PLUS <arith-expr1> | MINUS <arith-expr1> | LAMBDA
        # if <arith-op1> does not derive lambda return either a PlusNode or a MinusNode else just return the expression

        if not isinstance(arith_op1_children[0].symbol, Lambda):
            left_operant = expr_node  # use the expr_node as the left operant
            right_operant = self.visit_ARITH_EXPR_1(
                arith_op1_children[1])  # visit_ARITH_EXPR_1 to find the right operant

            if arith_op1_children[0].name == 'PLUS':
                return PlusNode(left_operant, right_operant)
            elif arith_op1_children[0].name == 'MINUS':
                return MinusNode(left_operant, right_operant)

        return expr_node

    def visit_ARITH_EXPR_2(self, node):
        # <arith-expr2> -> <arith-expr3>, <arith-op2>
        expr_node = self.visit_ARITH_EXPR_3(node.children[0])

        arith_op2_children = node.children[1].children
        # <arith-op2> -> MULT <arith-expr2> | DIVIDE <arith-expr2> | MODULO <arith-expr2> | LAMBDA
        # if <arith-op1> does not derive lambda return either a MultNode, DivideNode or ModuloNode
        # else just return the expression

        if not isinstance(arith_op2_children[0].symbol, Lambda):  # if <arith-op2> does not derive lambda
            left_operant = expr_node  # use the expr_node as the left operant
            right_operant = self.visit_ARITH_EXPR_2(
                arith_op2_children[1])  # visit_ARITH_EXPR_1 to find the right operant

            if arith_op2_children[0].name == 'MULT':
                return MultiplyNode(left_operant, right_operant)
            elif arith_op2_children[0].name == 'DIVIDE':
                return DivideNode(left_operant, right_operant)
            elif arith_op2_children[0].name == 'MODULO':
                return ModuloNode(left_operant, right_operant)

        return expr_node

    def visit_ARITH_EXPR_3(self, node):
        # <arith-expr3> -> <term> | LPAREN <expr> RPAREN | MINUS <arith-expr3> | NOT <arith-expr3>

        # call visit based on which node it is
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

        # call visit based on which node it is
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

        id = self.visit_ARRAY_REF(node.children[0])
        id_operator_children = node.children[1].children
        # <id-operator> -> <dot-ref> | LPAREN <params> RPAREN

        if id_operator_children[0].name == '<dot-ref>':
            if isinstance(id_operator_children[0].children[0].symbol, Lambda):
                return id

            id_list = []
            ids = self.visit_DOT_REF(id_operator_children[0])  # find the rest of the ids

            # append the initial id and the rest of the id's to a list
            id_list.append(id)
            id_list.extend(ids)
            return DotNode(id_list)  # create a DotNode using the list of ids

        elif id_operator_children[0].name == 'LPAREN':
            param_node = self.visit_ACTUAL_PARAMS(id_operator_children[1])  # visit_PARAMS to get the ParamNode
            return NewObjectNode(id, param_node)  # use the ParamNode to make a NewObejctNode and return it

    def visit_VAL(self, node):
        # visit either float or integer depending on the node
        child = node.children[0]
        if child.name == 'FLOAT':
            return self.visit_FLOAT(child)
        elif child.name == 'INTEGER':
            return self.visit_INT(child)

    def visit_INT(self, node):
        return IntegerNode(node.value)  # return IntegerNode with the value from the node

    def visit_BOOL(self, node):
        return BoolNode(node.value)  # return BoolNode with the value from the node

    def visit_STR(self, node):
        return StringNode(node.value)  # return StringNode with the value from the node

    def visit_FLOAT(self, node):
        return FloatNode(node.value)  # return FloatNode with the value from the node
