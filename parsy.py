from grammar import *
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
    def __init__(self, grammar):
        self.stack = Stack()
        self.grammar = grammar

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
        for nonterm in self.grammar.nonterminals.keys():
            inside_dict = {}
            for term in self.grammar.terminals.keys():
                inside_dict[term] = 0
            parse_table[nonterm] = inside_dict

        for rule in self.grammar.rules:
            predict_set = self.grammar.predict(rule)
            for terminal in predict_set:
                if parse_table[rule.LHS.name][terminal] == 0:
                    parse_table[rule.LHS.name][terminal] = rule.rule_nr

        return parse_table


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

for rule in grammar.rules:
    print(rule)

parser = Parser(grammar)
table = parser.create_parse_table()

print("Parse Table:")
print("  ", [x for x in table['S'].keys()])
for key in table.keys():
    print(f"{key}:", [str(x) for x in table[key].values()])

# print(Grammar.to_str())