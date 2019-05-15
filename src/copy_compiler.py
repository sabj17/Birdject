import os

from prettytable import PrettyTable

from codegen.program import Program
from codegen.visitor import Visitor
from src.symbol_table import AstNodeVisitor
from src.grammar import *
from src.lexer import Lexer
from src.parser import Parser

wd = os.getcwd()
grammar_file = os.path.join(wd, 'resources/grammar.txt')
program_file = os.path.join(wd, 'resources/Example.jnr')

grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

program = '''
    set dab to Thermometer();
'''

#print(grammar)

lexer = Lexer(program_file=program_file)
tokens = lexer.lex()

#print()
#print(",".join([str(x) for x in tokens]))

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
ast = parse_tree.to_AST()

ast.graph()
visitor = AstNodeVisitor()
ast.accept(visitor)
symtable = visitor.current_scope
print('The entire table:')
print(symtable.symbols)
#table = symtable.lookup('LivingRoomScope')
#something = table.lookup('temp1')
#print(something)

#something = symtable.lookup('fuck')

#codeVisitor = Visitor(Program(), symtable)
#codeVisitor.visit(ast.prog)
