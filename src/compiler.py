import os

from prettytable import PrettyTable

from codegen.program import Program
from codegen.visitor import Visitor
from src.symbol_table import AstNodeVisitor
from src.grammar import *
from src.lexer import Lexer
from src.parser import Parser
from src.parsetree import BuildASTVisitor
from src.ast import GraphASTVisitor

wd = os.getcwd()
grammar_file = os.path.join(wd, 'resources/grammar.txt')
program_file = os.path.join(wd, 'resources/TestButton.jnr')
keyword_file = os.path.join(wd, 'resources/keywords.txt')
token_spec_file = os.path.join(wd, 'resources/token_spec.txt')

grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

program = '''
    set dab to Thermometer();
'''

#print(grammar)

lexer = Lexer(program_file, keyword_file, token_spec_file)
tokens = lexer.lex()

# print("\n".join([str(x) for x in tokens]))

parser = Parser(grammar)

ptable = PrettyTable(['Nonterminals'] + list(grammar.terminals.keys()))
for val in parser.parse_table:
    row = []
    for key, value in parser.parse_table[val].items():
        row.append(value)
    ptable.add_row([val] + row)

#print("\n", ptable)

parse_tree = parser.parse(tokens)

parse_tree.graph()
ast = parse_tree.accept(BuildASTVisitor())



ast.accept(GraphASTVisitor())

visitor = AstNodeVisitor()
ast.accept(visitor)
symtable = visitor.current_scope

codeVisitor = Visitor(Program(), symtable)
codeVisitor.visit(ast.prog)