import abc


class Rule:

    def __init__(self, LHS, RHS):
        self.LHS = Grammar.get_symbol(LHS, 'non-terminals')
        self.RHS = Production(RHS)

    def __str__(self):
        return self.LHS.name + " -> " + self.RHS.__str__()

    def in_RHS(self, A):
        for symbol in self.RHS.symbols:
            if symbol.name == A:
                return True
        return False


class Production:

    def __init__(self, symbols):
        if len(symbols) == 1 and symbols[0] == 'λ':
            self.symbols = [Lambda()]
            self.is_lambda = True
        else:
            self.is_lambda = False
            self.symbols = [Grammar.get_symbol(symbol) for symbol in symbols]

    def __str__(self):
        return " ".join([symbol.name for symbol in self.symbols])

    def all_derive_empty(self):
        for X in self.symbols:
            if Grammar.symbolderivesempty(X.name) == False:
                return False
        return True

    def tail(self, A):
        ans = []
        found = False
        for symbol in self.symbols:
            if found:
                ans.append(symbol.name)
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
        symbol_names = [symbol.name for symbol in production.symbols]
        return Production(symbol_names)


class Symbol:

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def derives_empty(self):
        return False


class Terminal(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def derives_empty(self):
        return False


class Nonterminal(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def derives_empty(self):
        for rule in Grammar.rules:
            if rule.LHS.name == self.name:
                if rule.RHS.is_lambda:
                    return True
        return False


class Lambda(Symbol):

    def __init__(self):
        super().__init__('λ')

    def derives_empty(self):
        return True


class Grammar(object):
    terminals = {}
    nonterminals = {}
    rules = []

    @staticmethod
    def get_rules_for(A):
        ans = []
        for rule in Grammar.rules:
            if rule.LHS.name == A:
                ans.append(rule)
        return ans

    @staticmethod
    def add_rule(rule):
        Grammar.rules.append(rule)

    @staticmethod
    def to_str():
        return "\n".join(rule.__str__() for rule in Grammar.rules)

    @staticmethod
    def get_symbol(name, allowed='both'):
        if allowed == 'non-terminals' or allowed == 'both':
            if name in Grammar.nonterminals.keys():
                return Grammar.nonterminals[name]

        if allowed == 'terminals' or allowed == 'both':
            if name in Grammar.terminals.keys():
                return Grammar.terminals[name]

        return None

    @staticmethod
    def occurrence(A):
        ans = []
        for rule in Grammar.rules:
            if rule.in_RHS(A):
                ans.append(rule)
        return ans

    @staticmethod
    def symbolderivesempty(A):
        matches = [rule for rule in Grammar.rules if rule.LHS.name == A]
        p_derives_empty = True
        for rule in matches:
            rhs = rule.RHS.symbols

            for symbol in rhs:
                if isinstance(symbol, Nonterminal):
                    p_derives_empty = Grammar.symbolderivesempty(symbol.name)
                else:
                    p_derives_empty = symbol.derives_empty()

                if not p_derives_empty:
                    break

            if p_derives_empty:
                return True

        return p_derives_empty

    @staticmethod
    def first(production):
        visited_first = {}
        for nonterm in Grammar.nonterminals.keys():
            visited_first[nonterm] = False

        production = Production.get_copy(production)
        ans = Grammar._internalfirst(production, visited_first)
        return ans

    @staticmethod
    def _internalfirst(production, visited_first):
        ans = []
        if production.is_empty():  # empty array
            return set()

        first_symbol = production.pop_first_symbol().name

        # If the symbol is a terminal, it is returned
        if first_symbol in Grammar.terminals.keys():
            ans.append(first_symbol)
            return set(ans)

        # If the symbol is a nonterminal and hasn't been visited first

        if first_symbol != 'λ' and visited_first[first_symbol] is False:
            visited_first[first_symbol] = True
            # Gets the right hand side and calls it self recursively
            for rhs in [rule.RHS for rule in Grammar.get_rules_for(first_symbol)]:
                if rhs:
                    rhs = Production.get_copy(rhs)
                    ans.extend(Grammar._internalfirst(rhs, visited_first))

        # If the symbol derives to lambda
        if Grammar.symbolderivesempty(first_symbol):
            if production:
                ans.extend(Grammar._internalfirst(production, visited_first))

        return set(ans)

    @staticmethod
    def follow(A):
        visited_follow = {}
        for nonterm in Grammar.nonterminals.keys():
            visited_follow[nonterm] = False
        return Grammar._internalfollow(A, visited_follow)
    
    @staticmethod
    def _internalfollow(A, visited_follow):
        ans = []
        if visited_follow[A] is False:
            visited_follow[A] = True
            for rule in Grammar.occurrence(A):
                tail = rule.RHS.tail(A)
                ans.extend(Grammar.first(tail))
                if tail.all_derive_empty():
                    ans.extend(Grammar._internalfollow(rule.LHS.name, visited_follow))
        return set(ans)

    @staticmethod
    def predict(rule):
        ans = Grammar.first(rule.RHS)
        for a in ans:
            print("First: ", a)
        if rule.RHS.all_derive_empty():
            ans.update(Grammar.follow(rule.LHS.name))
        return ans

