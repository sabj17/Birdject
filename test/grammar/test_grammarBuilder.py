import os
from unittest import TestCase

from src.grammar import GrammarBuilder, Rule, Production, Nonterminal, Terminal, LAMBDA, Grammar


class TestGrammarBuilder(TestCase):

    @classmethod
    def setUpClass(cls):  # Before all tests
        cls.grammar_file = os.path.abspath(os.path.join('../..', 'src/resources/testgrammar.txt'))
        cls.grammar = GrammarBuilder.build_grammar_from_file(cls.grammar_file)
        cls.nonterminals = cls.grammar.nonterminals
        cls.terminals = cls.grammar.terminals
        cls.grammar_builder = GrammarBuilder()

    def setUp(self):  # Before each test
        # Set up of manual grammar builder
        self.grammar_builder_manual = GrammarBuilder()

        prog = Nonterminal('<prog>')
        stmts = Nonterminal('<stmts>')
        stmt = Nonterminal('<stmt>')
        whenstmt = Nonterminal('<when-stmt>')
        forstmt = Nonterminal('<for-stmt>')
        ifstmt = Nonterminal('<if-stmt>')
        vardcl = Nonterminal('<var-dcl>')
        expr = Nonterminal('<expr>')
        block = Nonterminal('<block>')
        elseclause = Nonterminal('<else-clause>')
        else_s = Nonterminal('<else>')
        blockbody = Nonterminal('<block-body>')
        blockbodypart = Nonterminal('<block-body-part>')
        dotref = Nonterminal('<dot-ref>')
        id = Nonterminal('<id>')

        dollar = Terminal('$')
        lambda_terminal = Terminal('λ')
        if_terminal = Terminal('IF')
        lparen_terminal = Terminal('LPAREN')
        rparen_terminal = Terminal('RPAREN')
        else_terminal = Terminal('ELSE')
        foreach_terminal = Terminal('FOREACH')
        in_terminal = Terminal('IN')
        when_terminal = Terminal('WHEN')
        lcurly_terminal = Terminal('LCURLY')
        rcurly_terminal = Terminal('RCURLY')
        set_terminal = Terminal('SET')
        to_terminal = Terminal('TO')
        end_terminal = Terminal('END')
        plus_terminal = Terminal('PLUS')
        minus_terminal = Terminal('MINUS')
        id_terminal = Terminal('ID')

        prog_prod = [stmts.name, dollar.name]
        stmts_prod_1 = [stmt.name, stmts.name]
        stmts_prod_2 = [lambda_terminal.name]
        stmt_prod_1 = [whenstmt.name]
        stmt_prod_2 = [forstmt.name]
        stmt_prod_3 = [ifstmt.name]
        stmt_prod_4 = [vardcl.name]
        ifstmt_prod = [if_terminal.name, lparen_terminal.name, expr.name, rparen_terminal.name, block.name, elseclause.name]
        elseclause_prod_1 = [else_terminal.name, else_s.name]
        elseclause_prod_2 = [lambda_terminal.name]
        else_prod_1 = [block.name]
        else_prod_2 = [ifstmt.name]
        forstmt_prod = [foreach_terminal.name, id.name, in_terminal.name, expr.name, block.name]
        whenstmt_prod = [when_terminal.name, lparen_terminal.name, expr.name, rparen_terminal.name, block.name]
        block_prod = [lcurly_terminal.name, blockbody.name, rcurly_terminal.name]
        blockbody_prod_1 = [blockbodypart.name, blockbody.name]
        blockbody_prod_2 = [lambda_terminal.name]
        blockbodypart_prod_1 = [forstmt.name]
        blockbodypart_prod_2 = [ifstmt.name]
        blockbodypart_prod_3 = [vardcl.name]
        vardcl_prod = [set_terminal.name, id.name, dotref.name, to_terminal.name, expr.name, end_terminal.name]
        expr_prod_1 = [plus_terminal.name, expr.name]
        expr_prod_2 = [minus_terminal.name, expr.name]
        dotref_prod = [lambda_terminal.name]
        id_prod = [id_terminal.name]

        self.grammar_builder_manual.add_rule(prog.name, prog_prod)
        self.grammar_builder_manual.add_rule(stmts.name, stmts_prod_1)
        self.grammar_builder_manual.add_rule(stmts.name, stmts_prod_2)
        self.grammar_builder_manual.add_rule(stmt.name, stmt_prod_1)
        self.grammar_builder_manual.add_rule(stmt.name, stmt_prod_2)
        self.grammar_builder_manual.add_rule(stmt.name, stmt_prod_3)
        self.grammar_builder_manual.add_rule(stmt.name, stmt_prod_4)
        self.grammar_builder_manual.add_rule(ifstmt.name, ifstmt_prod)
        self.grammar_builder_manual.add_rule(elseclause.name, elseclause_prod_1)
        self.grammar_builder_manual.add_rule(elseclause.name, elseclause_prod_2)
        self.grammar_builder_manual.add_rule(else_s.name, else_prod_1)
        self.grammar_builder_manual.add_rule(else_s.name, else_prod_2)
        self.grammar_builder_manual.add_rule(forstmt.name, forstmt_prod)
        self.grammar_builder_manual.add_rule(whenstmt.name, whenstmt_prod)
        self.grammar_builder_manual.add_rule(block.name, block_prod)
        self.grammar_builder_manual.add_rule(blockbody.name, blockbody_prod_1)
        self.grammar_builder_manual.add_rule(blockbody.name, blockbody_prod_2)
        self.grammar_builder_manual.add_rule(blockbodypart.name, blockbodypart_prod_1)
        self.grammar_builder_manual.add_rule(blockbodypart.name, blockbodypart_prod_2)
        self.grammar_builder_manual.add_rule(blockbodypart.name, blockbodypart_prod_3)
        self.grammar_builder_manual.add_rule(vardcl.name, vardcl_prod)
        self.grammar_builder_manual.add_rule(expr.name, expr_prod_1)
        self.grammar_builder_manual.add_rule(expr.name, expr_prod_2)
        self.grammar_builder_manual.add_rule(dotref.name, dotref_prod)
        self.grammar_builder_manual.add_rule(id.name, id_prod)

        self.builder_rules = self.grammar_builder_manual.rules

    #################
    #     TESTS     #
    #################
    #   test_add_*  #
    #################

    def test_add_terminals(self):
        self.grammar_builder.add_terminals(self.grammar.terminals)
        test_set = set(self.grammar_builder.terminals)

        self.assertEqual(test_set, {'LPAREN', 'LCURLY', 'FOREACH', '$', 'IN', 'RPAREN', 'IF',
                                     'WHEN', 'SET', 'TO', 'END', 'PLUS', 'ELSE', 'MINUS',
                                     'RCURLY', 'ID'})

    def test_add_nonterminals(self):
        self.grammar_builder.add_nonterminals(self.grammar.nonterminals)
        test_set = set(self.grammar_builder.nonterminals)
        self.assertEqual(test_set, {'<else-clause>', '<block-body>', '<prog>', '<stmt>', '<block>',
                                     '<when-stmt>', '<stmts>', '<else>', '<expr>', '<var-dcl>',
                                     '<if-stmt>', '<for-stmt>', '<block-body-part>', '<dot-ref>', '<id>'})

    def test_add_rule(self):
        # Construct rule for testing
        S = Nonterminal('<prog>')
        A = Nonterminal('<stmts>')
        dollar = Terminal('$')
        production = Production([A, dollar])
        test_rule = Rule(S, production)

        # Get lhs and rhs of rule. Lhs in string and rhs in list of strings. Add as rule to grammar_builder
        lhs = self.grammar.rules[0].LHS.name
        rhs = [symbol.name for symbol in self.grammar.rules[0].RHS.symbols]
        self.grammar_builder.add_rule(lhs, rhs)

        # Unpack grammar_builder rule of index 0
        x, y = self.grammar_builder.rules[0]
        x_nonterminal = Nonterminal(x)
        symbol_list = []

        # Make all strings from rhs into relevant symbol type
        for S in y:
            if S is not '$' and S is not LAMBDA and S.isupper:
                s_symbol = Nonterminal(S)
            else:
                s_symbol = Terminal(S)

            symbol_list.append(s_symbol)

        y_production = Production(symbol_list)
        builder_rule = Rule(x_nonterminal, y_production)
        self.assertEqual(builder_rule.__str__(), test_rule.__str__())

    def test_add_rules_from_file(self):
        test_builder = GrammarBuilder()
        test_builder.add_rules_from_file(self.grammar_file)

        self.assertEqual(test_builder.rules, [('<prog>', ['<stmts>', '$']),
                                              ('<stmts>', ['<stmt>', '<stmts>']),
                                              ('<stmts>', ['λ']), ('<stmt>', ['<when-stmt>']),
                                              ('<stmt>', ['<for-stmt>']), ('<stmt>', ['<if-stmt>']),
                                              ('<stmt>', ['<var-dcl>']),
                                              ('<if-stmt>', ['IF', 'LPAREN', '<expr>', 'RPAREN', '<block>', '<else-clause>']),
                                              ('<else-clause>', ['ELSE', '<else>']), ('<else-clause>', ['λ']),
                                              ('<else>', ['<block>']), ('<else>', ['<if-stmt>']),
                                              ('<for-stmt>', ['FOREACH', '<id>', 'IN', '<expr>', '<block>']),
                                              ('<when-stmt>', ['WHEN', 'LPAREN', '<expr>', 'RPAREN', '<block>']),
                                              ('<block>', ['LCURLY', '<block-body>', 'RCURLY']),
                                              ('<block-body>', ['<block-body-part>', '<block-body>']),
                                              ('<block-body>', ['λ']), ('<block-body-part>', ['<for-stmt>']),
                                              ('<block-body-part>', ['<if-stmt>']), ('<block-body-part>', ['<var-dcl>']),
                                              ('<var-dcl>', ['SET', '<id>', '<dot-ref>', 'TO', '<expr>', 'END']),
                                              ('<expr>', ['PLUS', '<expr>']), ('<expr>', ['MINUS', '<expr>']),
                                              ('<dot-ref>', ['λ']), ('<id>', ['ID'])])

    ###################
    # everything else #
    ###################

    def test_build_grammar_from_file(self):
        test_grammar_from_file = GrammarBuilder().build_grammar_from_file(self.grammar_file)
        grammar_string = '<prog> -> <stmts> $\n<stmts> -> <stmt> <stmts>\n<stmts> -> λ\n' \
                         '<stmt> -> <when-stmt>\n<stmt> -> <for-stmt>\n<stmt> -> <if-stmt>\n' \
                         '<stmt> -> <var-dcl>\n<if-stmt> -> IF LPAREN <expr> RPAREN <block> ' \
                         '<else-clause>\n<else-clause> -> ELSE <else>\n<else-clause> -> λ\n' \
                         '<else> -> <block>\n<else> -> <if-stmt>\n<for-stmt> -> FOREACH <id> IN ' \
                         '<expr> <block>\n<when-stmt> -> WHEN LPAREN <expr> RPAREN <block>' \
                         '\n<block> -> LCURLY <block-body> RCURLY\n<block-body> -> <block-body-part> ' \
                         '<block-body>\n<block-body> -> λ\n<block-body-part> -> <for-stmt>\n' \
                         '<block-body-part> -> <if-stmt>\n<block-body-part> -> <var-dcl>\n<var-dcl> ' \
                         '-> SET <id> <dot-ref> TO <expr> END\n<expr> -> PLUS <expr>\n<expr> -> ' \
                         'MINUS <expr>\n<dot-ref> -> λ\n<id> -> ID'

        self.assertEqual(test_grammar_from_file.__str__(), grammar_string)

    def test__find_nonterminals_from_rules(self):
        nonterminals_from_rules = self.grammar_builder_manual._find_nonterminals_from_rules(self.builder_rules)
        self.assertEqual(set(nonterminals_from_rules), set(self.nonterminals))

    def test__find_terminals_from_rules(self):
        terminals_from_rules = self.grammar_builder_manual._find_terminals_from_rules(self.builder_rules,
                                                                                      self.nonterminals)
        terminals_from_rules.remove('λ')
        terminal_names = [t for t in terminals_from_rules]
        self.assertEqual(set(terminal_names), set(self.terminals))

    def test__format_line(self):
        self.assertEqual(self.grammar_builder._format_line('S -> A, C, $', 1), ('S', ['A', 'C', '$']))
        self.assertEqual(self.grammar_builder._format_line('C -> LAMBDA', 1), ('C', ['λ']))
        self.assertEqual(self.grammar_builder._format_line('A -> a, B, C, d', 1), ('A', ['a', 'B', 'C', 'd']))
        self.assertEqual(self.grammar_builder._format_line('B -> b, B', 1), ('B', ['b', 'B']))
        self.assertEqual(self.grammar_builder._format_line('Q -> q', 1), ('Q', ['q']))

    def test_build(self):
        nonterminals_list = [nonterm for nonterm in self.grammar_builder_manual._find_nonterminals_from_rules(
            self.grammar_builder_manual.rules
        )]
        terminals_list = [term for term in self.grammar_builder_manual._find_terminals_from_rules(
            self.grammar_builder_manual.rules, nonterminals_list)]
        self.grammar_builder_manual.nonterminals = nonterminals_list
        self.grammar_builder_manual.terminals = terminals_list

        test_grammar = self.grammar_builder_manual.build()
        self.assertEqual(test_grammar.to_str(), self.grammar.to_str())

    def test__get_production(self):
        nonterminals_list = [nonterm for nonterm in self.grammar_builder_manual._find_nonterminals_from_rules(
            self.grammar_builder_manual.rules
        )]
        terminals_list = [term for term in self.grammar_builder_manual._find_terminals_from_rules(
            self.grammar_builder_manual.rules, nonterminals_list)]

        terminal_dict = {}
        nonterminal_dict = {}

        for terminal in terminals_list:
            terminal_dict[terminal] = Terminal(terminal)

        for nonterminal in nonterminals_list:
            nonterminal_dict[nonterminal] = Nonterminal(nonterminal)

        for rule in self.grammar.rules:
            lhs = rule.LHS.name
            rhs = [symbol.name for symbol in rule.RHS.symbols]
            self.grammar_builder.add_rule(lhs, rhs)

        LHS_1, RHS_1 = self.grammar_builder_manual.rules[0]
        LHS_2, RHS_2 = self.grammar_builder_manual.rules[5]
        LHS_3, RHS_3 = self.grammar_builder_manual.rules[10]
        LHS_4, RHS_4 = self.grammar_builder_manual.rules[15]
        print(LHS_4, RHS_4)

        test_production_1 = self.grammar_builder_manual._get_production(RHS_1, terminal_dict, nonterminal_dict)
        test_production_2 = self.grammar_builder_manual._get_production(RHS_2, terminal_dict, nonterminal_dict)
        test_production_3 = self.grammar_builder_manual._get_production(RHS_3, terminal_dict, nonterminal_dict)
        test_production_4 = self.grammar_builder_manual._get_production(RHS_4, terminal_dict, nonterminal_dict)

        self.assertEqual(test_production_1.__str__(), '<stmts> $')
        self.assertEqual(test_production_2.__str__(), '<if-stmt>')
        self.assertEqual(test_production_3.__str__(), '<block>')
        self.assertEqual(test_production_4.__str__(), '<block-body-part> <block-body>')
        self.assertNotEqual(test_production_4.__str__(), '<stmts>')
