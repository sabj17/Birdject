from grammar import Grammar, Terminal, Production, Nonterminal, Rule
from token import Token, TokenStream


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        return self.items.pop()

    def top_of_stack(self):
        return self.items[len(self.items)-1]


class Parser:
    def __init__(self):
        stack = Stack()

    def parse(self, tokens):
        pass

    def llparser(self, tokens):
        self.stack.push("S")
        ts = TokenStream(tokens)
        accepted = False
        while not accepted:
            if isinstance(self.stack.tos(), Terminal):  # is terminal
                self.match(ts, self.stack.tos())
                if self.stack.tos() == "$":
                    accepted = True
                self.stack.pop()
            else:
                p = 0  # LLtable[TOS( ), ts.peek( )]
                if p == 0:
                    print("Syntax error—no production applicable")
                else:
                    self.apply(p, self.stack)

    # Gotta change this func
    def apply(self, p, s):
        a = []
        s.pop()
        for x in range(len(a) - 1, 0):
            s.push(a[x])

    def match(self, ts, token):
        if ts.peek() == token:
            ts.advance()
        else:
            print("You fucked up")


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

       # for item in parse_table.items():
        #    print(item)

        return parse_table


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