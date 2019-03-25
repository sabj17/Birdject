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

    def __str__(self):
        return ", ".join([x.name for x in self.items])


class Parser:
    def __init__(self, grammar):
        self.stack = Stack()
        self.grammar = grammar
        self.parse_table = self.create_parse_table()

    def parse(self, tokens):
        pass

    def llparser(self, tokens):
        self.stack.push(Nonterminal("S"))
        ts = TokenStream(tokens)

        accepted = False
        while not accepted:
            tos = self.stack.top_of_stack()
            if isinstance(tos, Terminal):  # is terminal
                self.match(ts, tos)
                if tos.name == '$':
                    accepted = True
                self.stack.pop()
            else:
                rule_number = self.parse_table[tos.name][ts.peek().kind]
                if rule_number == 0:
                    print("Syntax error—no production applicable")
                else:
                    self.apply(rule_number, self.stack)

    def apply(self, rule_number, stack):
        stack.pop()

        rule = self.grammar.get_rule_from_line(rule_number)
        if rule.RHS.is_lambda:
            return

        for symbol in reversed(rule.RHS.symbols):  # iterates the list in reverse
            stack.push(symbol)

    def match(self, ts, symbol):
        if ts.peek().kind == symbol.name:
            print("Matched: ", ts.peek().kind)
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
