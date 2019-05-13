from unittest import TestCase

from src.codegen.codegen import CodeEmittor
from src.codegen.visitor import TopVisitor
from src.codegen.program import Program, Structure

from src.grammar import *
from src.symbol_table import SymbolTable
from src.tokens import Token
from src.parser import Parser
from src.lexer import Lexer
import os
from prettytable import PrettyTable


class TestCodeGenVisitor(TestCase):

    @classmethod
    def setUpClass(cls):


        grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/grammar.txt'))
        program_file = os.path.abspath(os.path.join('../..', 'src/resources/Example1.jnr'))


        grammar = GrammarBuilder.build_grammar_from_file(grammar_file)
        lexer = Lexer(file_path=program_file)
        tokens = lexer.lex()
        parser = Parser(grammar)
        parse_tree = parser.parse(tokens)

        cls.ast = parse_tree.to_AST()
        # ast.graph()

        # symtable = SymbolTable(ast)

    def test_class(self):
        program = Program()
        visitor = TopVisitor(program)
        self.ast.accept(visitor)








        hello = visitor.code_gen.stack
        #print("hello:")
        #print(hello)
        visitor.code_gen.generate_tcode()


