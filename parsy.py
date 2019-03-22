from grammar import Grammar, Terminal, Production, Nonterminal, Rule


class Parser:
    def __init__(self):
        pass

    def parse(self, tokens):
        pass

    def create_parse_table(self):
        parse_table = {}
        for nonterm in Grammar.nonterminals.keys():
            inside_dict = {}
            for term in Grammar.terminals.keys():
                inside_dict[term] = 0
            parse_table[nonterm] = inside_dict

        for rule in Grammar.rules:
            predict_set = Grammar.predict(rule)
            for terminal in predict_set:
                if parse_table[rule.LHS.name][terminal] == 0:
                    parse_table[rule.LHS.name][terminal] = rule.rule_nr

        return parse_table
        # for item in parse_table.items():
            # print(item)


Grammar.terminals = {'a': Terminal('a'), 'b': Terminal('b'), 'c': Terminal('c'), 'd': Terminal('d'), 'q': Terminal('q'), '$': Terminal('$')}
Grammar.nonterminals = {'A': Nonterminal('A'), 'B': Nonterminal('B'), 'C': Nonterminal('C'), 'Q': Nonterminal('Q'), 'S': Nonterminal('S')}
Grammar.add_rule(Rule('S', ['A', 'C', '$']))
Grammar.add_rule(Rule('C', ['c']))
Grammar.add_rule(Rule('C', ['λ']))
Grammar.add_rule(Rule('A', ['a', 'B', 'C', 'd']))
Grammar.add_rule(Rule('A', ['B', 'Q']))
Grammar.add_rule(Rule('B', ['b', 'B']))
Grammar.add_rule(Rule('B', ['λ']))
Grammar.add_rule(Rule('Q', ['q']))
Grammar.add_rule(Rule('Q', ['λ']))


p = Production(['Q'])
ans = Grammar.predict(Rule('B', ['λ']))
#ans = Grammar.follow('B')

parser = Parser()
parser.create_parse_table()


# print(Grammar.to_str())