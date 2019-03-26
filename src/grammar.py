import abc

LAMBDA = 'λ'

class Rule:
    rule_count = 1

    def __init__(self, LHS, RHS):
        self.LHS = LHS
        self.RHS = RHS
        self.rule_nr = self.rule_count
        Rule.rule_count += 1

    def __str__(self):
        return self.LHS.name + " -> " + self.RHS.__str__()

    def in_RHS(self, A):
        for symbol in self.RHS.symbols:
            if symbol.name == A:
                return True
        return False


class Production:

    def __init__(self, symbols):
        self.symbols = symbols
        if len(symbols) == 1 and isinstance(symbols[0], Lambda):
            self.is_lambda = True
        else:
            self.is_lambda = False

    def __str__(self):
        return " ".join([symbol.name for symbol in self.symbols])

    def all_derive_empty(self, rules):
        if self.symbols is None:
            return True

        for symbol in self.symbols:
            if symbol.derives_empty(rules) is False:
                return False
        return True

    def tail(self, A):
        ans = []
        found = False
        for symbol in self.symbols:
            if found:
                ans.append(symbol)
            if symbol.name == A:
                found = True
        return Production(ans)

    def pop_first_symbol(self):
        return self.symbols.pop(0)

    def is_empty(self):
        if self.symbols:
            return False
        return True

    @staticmethod
    def get_copy(production):
        return Production(list(production.symbols))


class Symbol:

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def derives_empty(self, rules):
        return False


class Terminal(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def derives_empty(self, rules):
        return False


class Nonterminal(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def derives_empty(self, rules):
        matches = [rule for rule in rules if rule.LHS.name == self.name]

        p_derives_empty = True
        for rule in matches:
            rhs = rule.RHS.symbols

            for symbol in rhs:
                if symbol.name == self.name:
                    p_derives_empty = False
                else:
                    p_derives_empty = symbol.derives_empty(rules)

                if p_derives_empty is False:
                    break

            if p_derives_empty:
                return True

        return p_derives_empty


class Lambda(Symbol):

    def __init__(self):
        super().__init__(LAMBDA)

    def derives_empty(self, rules):
        return True


class Grammar:

    def __init__(self, terminals, nonterminals, rules):
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.rules = rules
        self.start_symbol = rules[0].LHS

    def get_rules_for(self, A):
        ans = []
        for rule in self.rules:
            if rule.LHS.name == A:
                ans.append(rule)
        return ans

    def get_rule_from_line(self, line_number):
        for rule in self.rules:
            if rule.rule_nr == line_number:
                return rule
        return None

    def to_str(self):
        return "\n".join(rule.__str__() for rule in self.rules)

    def get_symbol(self, name, allowed='both'):
        if allowed == 'non-terminals' or allowed == 'both':
            if name in self.nonterminals.keys():
                return self.nonterminals[name]

        if allowed == 'terminals' or allowed == 'both':
            if name in self.terminals.keys():
                return self.terminals[name]

        return None

    def occurrence(self, symbol):
        ans = []
        for rule in self.rules:
            if rule.in_RHS(symbol):
                ans.append(rule)
        return ans

    def first(self, production):
        visited_first = {}
        for nonterm in self.nonterminals.keys():
            visited_first[nonterm] = False

        production = Production.get_copy(production)
        ans = self._internalfirst(production, visited_first)
        return ans

    def _internalfirst(self, production, visited_first):
        ans = []
        if production.is_empty():  # empty array
            return set()

        first_symbol = production.pop_first_symbol()

        # If the symbol is a terminal, it is returned
        if first_symbol.name in self.terminals.keys():
            ans.append(first_symbol.name)
            return set(ans)

        # If the symbol is a nonterminal and hasn't been visited first

        if first_symbol.name != LAMBDA and visited_first[first_symbol.name] is False:
            visited_first[first_symbol.name] = True
            # Gets the right hand side and calls it self recursively
            for rhs in [rule.RHS for rule in self.get_rules_for(first_symbol.name)]:
                if rhs:
                    rhs = Production.get_copy(rhs)
                    ans.extend(self._internalfirst(rhs, visited_first))

        # If the symbol derives to lambda
        if first_symbol.derives_empty(self.rules):
            if production:
                ans.extend(self._internalfirst(production, visited_first))

        return set(ans)

    def follow(self, A):
        visited_follow = {}
        for nonterm in self.nonterminals.keys():
            visited_follow[nonterm] = False
        return self._internalfollow(A, visited_follow)

    def _internalfollow(self, A, visited_follow):
        ans = []
        if visited_follow[A] is False:
            visited_follow[A] = True
            for rule in self.occurrence(A):
                tail = rule.RHS.tail(A)
                ans.extend(self.first(tail))
                if tail.all_derive_empty(self.rules):
                    ans.extend(self._internalfollow(rule.LHS.name, visited_follow))
        return set(ans)

    def predict(self, rule):
        ans = self.first(rule.RHS)
        if rule.RHS.all_derive_empty(self.rules):
            ans.update(self.follow(rule.LHS.name))
        return ans


class GrammarBuilder:

    def __init__(self):
        self.terminals = []
        self.nonterminals = []
        self.rules = []

    def add_terminals(self, terminal_list):
        # input: ['a', 'b', 'c']
        self.terminals += terminal_list

    def add_nonterminals(self, nonterminal_list):
        # input: ['A', 'B', 'C']
        self.nonterminals += nonterminal_list

    def add_rule(self, LHS, RHS):
        # input: RHS='A', LHS=['a','b','c']
        self.rules.append((LHS, RHS))

    @staticmethod
    def build_grammar_from_file(file_path):
        res = GrammarBuilder()
        res.add_rules_from_file(file_path)

        res.nonterminals = GrammarBuilder._find_nonterminals_from_rules(res.rules)
        res.terminals = GrammarBuilder._find_terminals_from_rules(res.rules, res.nonterminals)

        return res.build()

    @staticmethod
    def _find_nonterminals_from_rules(rules):
        nonterms = set()
        for lhs, _ in rules:
            nonterms.add(lhs)
        return list(nonterms)

    @staticmethod
    def _find_terminals_from_rules(rules, nonterminals):
        terminals = set()
        for _, rhs in rules:
            for symbol in rhs:
                if symbol not in nonterminals:
                    terminals.add(symbol)

        return list(terminals)

    def add_rules_from_file(self, file):
        with open(file, 'r') as rules_file:
            for index, line in enumerate(rules_file, start=1):
                lhs, rhs = self._format_line(line, index)

                if lhs and rhs:
                    self.add_rule(lhs, rhs)

    def _format_line(self, line, index):
        string = line.replace(' ', '')
        string = string.replace('\n', '')
        string = string.replace('LAMBDA', LAMBDA)

        split = string.split("->", maxsplit=2)

        if len(split) != 2:
            raise Exception(f'Error in grammar: line {index}')

        lhs, rhs = split
        rhs = rhs.split(',')

        return lhs, rhs

    def build(self):
        terminal_dict = {}
        nonterminal_dict = {}
        rule_list = []

        for terminal in self.terminals:
            terminal_dict[terminal] = Terminal(terminal)

        for nonterminal in self.nonterminals:
            nonterminal_dict[nonterminal] = Nonterminal(nonterminal)

        for LHS, RHS in self.rules:
            lhs = nonterminal_dict[LHS]
            rule_list.append(Rule(lhs, self._get_production(RHS, terminal_dict, nonterminal_dict)))

        return Grammar(terminal_dict, nonterminal_dict, rule_list)

    def _get_production(self, symbols_strings, terminal_dict, nonterminal_dict):
        if len(symbols_strings) == 1 and symbols_strings[0] == LAMBDA:
            return Production([Lambda()])

        actual_symbols = []
        for symbol in symbols_strings:
            if symbol in terminal_dict:
                actual_symbols.append(terminal_dict[symbol])
            elif symbol in nonterminal_dict:
                actual_symbols.append(nonterminal_dict[symbol])
            else:
                raise Exception('Unknown symbol')  # TODO: change this to be better
        return Production(actual_symbols)
