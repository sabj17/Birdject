from grammar import Grammar, Terminal, Production, Nonterminal, Rule


class Parser:
    def __init__(self):
        pass

    def parse(self, tokens):
        pass

    def create_parse_table(self):
        parse_table = [[0 for _ in range(len(Grammar.terminals))] for _ in range(len(Grammar.nonterminals))]


        for list in parse_table:
            print(list, "\n")

Grammar.terminals = {'a': Terminal('a'), 'b': Terminal('b'), 'c': Terminal('c'), 'd': Terminal('d'), 'q': Terminal('q')}
Grammar.nonterminals = {'A': Nonterminal('A'), 'B': Nonterminal('B'), 'C': Nonterminal('C'), 'Q': Nonterminal('Q'), 'S': Nonterminal('S')}
Grammar.add_rule(Rule('S', ['A', 'C']))
Grammar.add_rule(Rule('A', ['a', 'B', 'C', 'd']))
Grammar.add_rule(Rule('A', ['B', 'Q']))
Grammar.add_rule(Rule('B', ['b', 'B']))
Grammar.add_rule(Rule('B', ['λ']))
Grammar.add_rule(Rule('C', ['c']))
Grammar.add_rule(Rule('C', ['λ']))
Grammar.add_rule(Rule('Q', ['q']))
Grammar.add_rule(Rule('Q', ['λ']))


p = Production(['Q'])
ans = Grammar.predict(Rule('B', ['λ']))
#ans = Grammar.follow('B')

parser = Parser()
parser.create_parse_table()

# print(Grammar.to_str())