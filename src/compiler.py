from src.grammar import *
from src.lexer import *
from src.token import Token
from src.parser import Parser
import os
from prettytable import PrettyTable

wd = os.getcwd()
grammar_file = os.path.join(wd, 'resources/grammar.txt')

grammar = GrammarBuilder.build_grammar_from_file(grammar_file)

#for n in grammar.terminals:
    #print(n)

parser = Parser(grammar)

#print("Parse table")
ptable = PrettyTable(['Nonterminals'] + list(grammar.terminals.keys()))

for val in parser.parse_table:
    row = []
    for key, value in parser.parse_table[val].items():
        row.append(value)
    ptable.add_row([val] + row)

#print(ptable)


print("\nMatches:")

string = 'set string to "hello " + "there";'
lexer = Lexer(program_string=string)
tokens = lexer.lex()
print("\n".join([str(x) for x in tokens]))

parser.parse(tokens)