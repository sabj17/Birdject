from src.grammar import *
from src.tokens import Token, TokenStream
from src.parsetree import *


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
        start = self.grammar.start_symbol
        self.stack.push(start)
        parse_tree = Tree(Node(start, None))
        ts = TokenStream(tokens)

        accepted = False
        while not accepted:
            tos = self.stack.top_of_stack()
            if isinstance(tos, Terminal):  # The next symbol is terminal
                self.match(ts, tos, parse_tree)
                if tos.name == '$':  # EOF symbol reached and loop is stopped
                    accepted = True
                self.stack.pop()
            else:  # Top of stack is a non terminal
                rule_number = self.parse_table[tos.name][ts.peek().kind]
                if rule_number == 0:
                    raise Exception(f"Syntax error — no production applicable for {tos.name} and {ts.peek().kind}: {ts.peek()}")
                else:  # Applies the RHS to the stack
                    self.apply(rule_number, self.stack, parse_tree)

        return parse_tree

    # Adds a rules RHS to the stack after popping the LHS from the stack
    def apply(self, rule_number, stack, parse_tree):
        stack.pop()
        rule = self.grammar.get_rule_from_line(rule_number)

        # Making nodes for parse tree
        nodes = []
        for symbol in rule.RHS.symbols:
            node = Node(symbol, None)
            nodes.append(node)
        parse_tree.add_nodes(nodes)

        if rule.RHS.is_lambda:
            return
        # Adds the RHS symbol in reverse to the stack, to be in the right order
        for symbol in reversed(rule.RHS.symbols):
            stack.push(symbol)

    # Checks if the next token matches with the symbol at TOS
    def match(self, ts, symbol, parse_tree):
        parse_tree.leaf_found(ts.peek().value)
        print(ts.peek(), symbol.name)
        if ts.peek().kind == symbol.name:
            ts.advance()
        else:
            raise Exception("stop ad hoc")

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
                    parse_table[rule.LHS.name][terminal] = rule.rule_num
                else:
                    raise Exception("Grammar not LL(1)")

        return parse_table
