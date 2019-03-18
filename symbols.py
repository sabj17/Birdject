class Symbol:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Terminal(Symbol):
    def __init__(self, name):
        super().__init__(name)


class Nonterminal(Symbol):
    visitedfirst = False
    derivesempty = False
    productions = []

    def __init__(self, name, productions):
        super().__init__(name)
        self.productions = productions
