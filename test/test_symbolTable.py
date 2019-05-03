from unittest import TestCase
from src.symbol_table import *


class TestSymbolTable(TestCase):
    def setUp(self):
        self.symtable = SymbolTable()
        self.visitor = AstNodeVisitor()

    def test_open_scope(self):  # TODO: assert something when open_scope has been fixed for keys/values
        self.symtable.add_symbol('simon')
        self.symtable.add_symbol('whoosmaus')
        block_node = BlockNode([AssignNode(IdNode('xyz'), UnaryExpNode('4'))])
        self.symtable.open_scope(self.visitor, block_node)
        self.symtable.add_symbol('jener')
        #print(self.symtable.current_scope)
        #self.assertEqual()

    def test_close_scope(self):
        self.test_open_scope()

    def test_set_current_scope_and_close_scope(self):
        self.symtable.scope_stack = Stack()
        self.assertEqual({}, self.symtable.current_scope)

        scope_1 = {'simon'}
        self.symtable.scope_stack.push(scope_1)
        self.symtable.set_current_scope()
        self.assertEqual({'simon'}, self.symtable.current_scope)

        scope_2 = {'whoosmaus', 'madidas'}
        self.symtable.scope_stack.push(scope_2)
        self.symtable.set_current_scope()
        self.assertEqual({'madidas', 'whoosmaus'}, self.symtable.current_scope)

        scope_3 = {'jener'}
        self.symtable.scope_stack.push(scope_3)
        self.symtable.set_current_scope()
        self.assertEqual({'jener'}, self.symtable.current_scope)

        # Close scope stuff
        self.symtable.close_scope()
        self.assertEqual({'madidas', 'whoosmaus'}, self.symtable.current_scope)

        self.symtable.close_scope()
        self.assertEqual({'simon'}, self.symtable.current_scope)

    def test_add_symbol(self):
        pass

    def test_get_symbol(self):
        pass

    def test_is_declared_locally(self):
        pass
