from src.ast import ProgNode, StatementNode, ExpressionNode, BlockNode, ActualParameterNode, FormalParameterNode,  TermNode, ClassNode, \
    ClassBodyNode, IdNode, IfNode, WhenNode, ForNode, AssignNode, FunctionNode, BinaryExpNode, UnaryExpNode, NotNode, \
    NegativeNode, ParenthesesNode, NewObjectNode, PlusNode, MinusNode, MultiplyNode, DivideNode, ModuloNode, EqualsNode, \
    NotEqualNode, GreaterThanNode, LessThanNode, AndNode, OrNode, BlockBodyPartNode, ReturnNode, BreakNode, RunNode, \
    BoolNode, StringNode, FloatNode, IntegerNode, DotNode, ArrayRefNode, AbstractNode
from src.codegen.codegen import CodeEmittor as CodeGen, CodeEmittor
from src.codegen.program import Structure

#Hello maddi daddi
class NodeVisitor2:

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__

        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)

        node.visit_children(self)

class Visitor(NodeVisitor):

    def __init__(self, program):
        #self.code_gen = CodeEmittor()
        self.program = program
        #self.structure = Structure(program)

    def visit_ProgNode(self, node):
        statements = vars(node).get("stmts")
        print("Program start")
        for node in statements:
            node.accept(self)
        print("Program end")

    def visit_ClassNode(self, node):
        print("Class start")
        self.program.new_class()
        class_atb = vars(node)
        class_id = class_atb.get("id")
        class_id.accept(self)
        print("{")
        self.accept_children(class_atb.get("body_part"))
        self.program.end_structure()
        print("Class end")

    def visit_IdNode(self, node):
        field = vars(node)
        key = field.keys()
        for k in key:
            self.program.emit_id(field.get(k))
            print("id: " + field.get(k))

    def visit_BlockNode(self, node):
        block_atb = vars(node)
        parts = block_atb.get("parts")
        for child in parts:
            child.accept(self)

    def visit_BlockBodyPartNode(self, node):
        part_atb = vars(node)
        key = part_atb.keys()
        for k in key:
            print("part: " + part_atb.get(k))

    def visit_ClassBodyNode(self, node):
        print("class body")
        body_atb = vars(node)
        self.accept_children(body_atb.get("body_parts"))

    def visit_AssignNode(self, node):
        string = ""
        assign_atb = vars(node)
        assign_id = assign_atb.get("id")
        self.code_gen.emit_id(assign_id)
        self.accept_children(assign_id, assign_atb.get("expression"))

        return string


    def visit(self, node):
        pass


    def accept_children(self, children):
        if isinstance(children, AbstractNode):
            children.accept(self)
        elif isinstance(children, list):
            for child in children:
                child.accept(self)







'''
class TopVisitor(NodeVisitor):

    def __init__(self, program):
        self.code_gen = CodeEmittor()
        self.program = program
        self.structure = Structure(program)

    @dispatch(ProgNode)
    def visit(self, node):
        self.structure.begin_structure()
        statements = vars(node).get("stmts")
        for node in statements:
            node.accept(self)

    @dispatch(ClassNode)
    def visit(self, node):
        class_atb = vars(node)
        class_id = class_atb.get("id")
        self.code_gen.emit_class_name(class_id)
        self.accept_children(class_id, class_atb.get("body_part"))

    @dispatch(FunctionNode)
    def visit(self, node):
        function_atb = vars(node)
        function_id = function_atb.get("id")
        function_params = function_atb.get("params")
        function_block = function_atb.get("block")

        self.code_gen.emit_func()
        function_id.accept(self)
        function_params.accept(self)
        self.accept_children(function_id, function_block)

    @dispatch(AssignNode)
    def visit(self, node):
        assign_atb = vars(node)
        assign_id = assign_atb.get("id")
        self.code_gen.emit_id(assign_id)
        self.accept_children(assign_id, assign_atb.get("expression"))

    @dispatch(RunNode)
    def visit(self, node):
        self.code_gen.emit_run()
        run_atb = vars(node)
        run_id = run_atb.get("id")
        run_params = run_atb.get("params")
        run_id.accept(self)
        if run_params is not None:
            run_params.accept(self)
        self.code_gen.emit_end("function_call")


    @dispatch(IfNode)
    def visit(self, node):
        if_atb = vars(node)
        if_true = if_atb.get("statement_true")
        if_false = if_atb.get("statement_false")
        self.code_gen.emit_if_vals(if_true, if_false)
        self.accept_children("if", if_atb.get("expression"))

    @dispatch(ForNode)
    def visit(self, node):
        for_atb = vars(node)
        for_id = for_atb.get("id")
        self.accept_children(for_id, for_atb.get("expression"))
        self.accept_children(for_id, for_atb.get("block"))

    @dispatch(WhenNode)
    def visit(self, node):
        when_atb = vars(node)
        self.accept_children("When", when_atb.get("expression"))
        self.accept_children("When", when_atb.get("block"))

    @dispatch(BlockNode)
    def visit(self, node):
        block_atb = vars(node)
        parts = block_atb.get("parts")
        for child in parts:
            child.accept(self)

    @dispatch(BlockBodyPartNode)
    def visit(self, node):
        self.code_gen.emit_block_body()

    @dispatch(ActualParameterNode) #hello
    def visit(self, node):
        self.code_gen.emit_parameters()
        expr_list = vars(node).get("expr_list")
        for child in expr_list:
            child.accept(self)
        self.code_gen.emit_end("Param")

    @dispatch(ExpressionNode)
    def visit(self, node):
        self.code_gen.emit_expression()

    @dispatch(BinaryExpNode)
    def visit(self, node):
        self.code_gen.emit_binary_exp()

    @dispatch(UnaryExpNode)
    def visit(self, node):
        self.code_gen.emit_unary_exp()

    @dispatch(NotNode)
    def visit(self, node):
        self.code_gen.emit_not_exp()

    @dispatch(NegativeNode)
    def visit(self, node):
        self.code_gen.emit_negative_exp()

    @dispatch(ParenthesesNode)
    def visit(self, node):
        self.code_gen.emit_paren_exp()

    @dispatch(NewObjectNode)
    def visit(self, node):
        self.code_gen.emit_new_obj_exp()

    @dispatch(PlusNode)
    def visit(self, node):
        self.code_gen.emit_plus_exp()
        expr = vars(node)
        for key in expr.keys():
            expr.get(key).accept(self)
        self.code_gen.emit_end("plus_exp")

    @dispatch(MinusNode)
    def visit(self, node):
        self.code_gen.emit_minus_exp()

    @dispatch(MultiplyNode)
    def visit(self, node):
        self.code_gen.emit_mult_exp()

    @dispatch(DivideNode)
    def visit(self, node):
        self.code_gen.emit_div_exp()

    @dispatch(ModuloNode)
    def visit(self, node):
        self.code_gen.emit_mod_exp()

    @dispatch(EqualsNode)
    def visit(self, node):
        self.code_gen.emit_equals_exp()

    @dispatch(NotEqualNode)
    def visit(self, node):
        self.code_gen.emit_not_equals_exp()

    @dispatch(GreaterThanNode)
    def visit(self, node):
        self.code_gen.emit_greater_than_exp()

    @dispatch(LessThanNode)
    def visit(self, node):
        self.code_gen.emit_less_than_exp()

    @dispatch(AndNode)
    def visit(self, node):
        self.code_gen.emit_and_exp()

    @dispatch(OrNode)
    def visit(self, node):
        self.code_gen.emit_or_exp()

    @dispatch(IdNode)
    def visit(self, node):
        field = vars(node)
        key = field.keys()
        for k in key:
            self.code_gen.emit_id(field.get(k))

    ##############
    # TERM STUFF #
    ##############

    @dispatch(TermNode)
    def visit(self, node):
        self.code_gen.emit_terminal()

    @dispatch(BoolNode)
    def visit(self, node):
        self.code_gen.emit_bool()

    @dispatch(StringNode)
    def visit(self, node):
        self.code_gen.emit_string()

    @dispatch(FloatNode)
    def visit(self, node):
        self.code_gen.emit_float()

    @dispatch(IntegerNode)
    def visit(self, node):
        field = vars(node)
        self.code_gen.emit_integer(field.get("value"))

    @dispatch(DotNode)
    def visit(self, node):
        self.code_gen.emit_dot()
        ids = vars(node).get("ids")
        for id1 in ids:
            id1.accept(self)
        self.code_gen.emit_end("dot")

    @dispatch(ArrayRefNode)
    def visit(self, node):
        self.code_gen.emit_array_ref()

    @dispatch(object)
    def visit(self, node):
        pass

    def accept_children(self, cnode_id, children):
        if isinstance(children, AbstractNode):
            children.accept(self)
        elif isinstance(children, list):
            for child in children:
                child.accept(self)
        self.code_gen.emit_end(cnode_id)

'''

'''
class CodeGenVisitor(NodeVisitor):

    def __init__(self):
        self.code_gen = CodeEmittor()

    @dispatch(ProgNode)
    def visit(self, node):
        self.code_gen.emit_prog()

    @dispatch(object)
    def visit(self, node):
        pass

    ##############
    # STATEMENTS #
    ##############

    @dispatch(StatementNode)
    def visit(self, node):
        self.code_gen.emit_statement()

    @dispatch(IfNode)
    def visit(self, node):
        self.code_gen.emit_if()

    @dispatch(WhenNode)
    def visit(self, node):
        self.code_gen.emit_when()

    @dispatch(ForNode)
    def visit(self, node):
        self.code_gen.emit_for()

    @dispatch(AssignNode)
    def visit(self, node):
        self.code_gen.emit_assign()

    @dispatch(FunctionNode)
    def visit(self, node):
        self.code_gen.emit_func()

    @dispatch(ClassNode)
    def visit(self, node):
        self.code_gen.emit_class()

    @dispatch(ClassBodyNode)
    def visit(self, node):
        self.code_gen.emit_class_body()

    ###############
    # EXPRESSIONS #
    ###############

    @dispatch(ExpressionNode)
    def visit(self, node):
        self.code_gen.emit_expression()

    @dispatch(BinaryExpNode)
    def visit(self, node):
        self.code_gen.emit_binary_exp()

    @dispatch(UnaryExpNode)
    def visit(self, node):
        self.code_gen.emit_unary_exp()

    @dispatch(NotNode)
    def visit(self, node):
        self.code_gen.emit_not_exp()

    @dispatch(NegativeNode)
    def visit(self, node):
        self.code_gen.emit_negative_exp()

    @dispatch(ParenthesesNode)
    def visit(self, node):
        self.code_gen.emit_paren_exp()

    @dispatch(NewObjectNode)
    def visit(self, node):
        self.code_gen.emit_new_obj_exp()

    @dispatch(PlusNode)
    def visit(self, node):
        self.code_gen.emit_plus_exp()

    @dispatch(MinusNode)
    def visit(self, node):
        self.code_gen.emit_minus_exp()

    @dispatch(MultiplyNode)
    def visit(self, node):
        self.code_gen.emit_mult_exp()

    @dispatch(DivideNode)
    def visit(self, node):
        self.code_gen.emit_div_exp()

    @dispatch(ModuloNode)
    def visit(self, node):
        self.code_gen.emit_mod_exp()

    @dispatch(EqualsNode)
    def visit(self, node):
        self.code_gen.emit_equals_exp()

    @dispatch(NotEqualNode)
    def visit(self, node):
        self.code_gen.emit_not_equals_exp()

    @dispatch(GreaterThanNode)
    def visit(self, node):
        self.code_gen.emit_greater_than_exp()

    @dispatch(LessThanNode)
    def visit(self, node):
        self.code_gen.emit_less_than_exp()

    @dispatch(AndNode)
    def visit(self, node):
        self.code_gen.emit_and_exp()

    @dispatch(OrNode)
    def visit(self, node):
        self.code_gen.emit_or_exp()

    ###############
    # BLOCK STUFF #
    ###############

    @dispatch(BlockNode)
    def visit(self, node):
        self.code_gen.emit_block()

    @dispatch(BlockBodyPartNode)
    def visit(self, node):
        self.code_gen.emit_block_body()

    @dispatch(ReturnNode)
    def visit(self, node):
        self.code_gen.emit_return()

    @dispatch(BreakNode)
    def visit(self, node):
        self.code_gen.emit_break()

    @dispatch(RunNode)
    def visit(self, node):
        self.code_gen.emit_run()

    ###################
    # PARAMETER STUFF #
    ###################

    @dispatch(ActualParameterNode)
    def visit(self, node):
        self.code_gen.emit_parameters()

    ##############
    # TERM STUFF #
    ##############

    @dispatch(TermNode)
    def visit(self, node):
        self.code_gen.emit_terminal()

    @dispatch(BoolNode)
    def visit(self, node):
        self.code_gen.emit_bool()

    @dispatch(StringNode)
    def visit(self, node):
        self.code_gen.emit_string()

    @dispatch(FloatNode)
    def visit(self, node):
        self.code_gen.emit_float()

    @dispatch(IntegerNode)
    def visit(self, node):
        field = vars(node)
        self.code_gen.emit_integer(field.get("value"))

    @dispatch(IdNode)
    def visit(self, node):
        field = vars(node)
        key = field.keys()
        for k in key:
            self.code_gen.emit_id(field.get(k))

    @dispatch(DotNode)
    def visit(self, node):
        self.code_gen.emit_dot()

    @dispatch(ArrayRefNode)
    def visit(self, node):
        self.code_gen.emit_array_ref()
'''