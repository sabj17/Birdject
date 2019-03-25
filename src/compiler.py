from src.grammar import *
from src.token import Token
from src.parser import Parser


grammarbuilder = GrammarBuilder()
grammarbuilder.add_terminals(['a', 'b', 'c', 'd', 'q', '$'])
grammarbuilder.add_nonterminals(['S', 'A', 'B', 'C', 'Q'])

grammarbuilder.add_rule('S', ['A', 'C', '$'])
grammarbuilder.add_rule('C', ['c'])
grammarbuilder.add_rule('C', [LAMBDA])
grammarbuilder.add_rule('A', ['a', 'B', 'C', 'd'])
grammarbuilder.add_rule('A', ['B', 'Q'])
grammarbuilder.add_rule('B', ['b', 'B'])
grammarbuilder.add_rule('B', [LAMBDA])
grammarbuilder.add_rule('Q', ['q'])
grammarbuilder.add_rule('Q', [LAMBDA])

grammar = grammarbuilder.build()

print(grammar.to_str())

parser = Parser(grammar)
table = parser.create_parse_table()

print("\nParse Table:")
print("  ", [x for x in table['S'].keys()])
for key in table.keys():
    print(f"{key}:", [str(x) for x in table[key].values()])

print("\nMatches:")

tokens = []
token_names = ['b', 'q', 'c', '$']

for x in token_names:
    tokens.append(Token(x, 0, 0, 0))


parser.parse(tokens)