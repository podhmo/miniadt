# -*- coding:utf-8 -*-
import unittest


class EqualityTest(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from miniadt import ADTTypeProvider
        return ADTTypeProvider(*args, **kwargs)

    def test_with_completely_different_type(self):
        T1 = self._makeOne('T1')
        C1 = T1('C1', '')
        T2 = self._makeOne('T2')
        C2 = T2('C2', '')

        self.assertNotEqual(C1(), C2())

    def test_with_diferent_type(self):
        List = self._makeOne('List')
        Cons = List('Cons', 'head tail')
        Cons2 = List('Cons2', 'head tail')
        Nil = List('Nil', '')

        self.assertNotEqual(Cons(1, Nil()), Cons2(1, Nil()))

    def test_with_same_type(self):
        List = self._makeOne('List')
        Cons = List('Cons', 'head tail')
        Nil = List('Nil', '')

        self.assertEqual(Cons(1, Nil()), Cons(1, Nil()))

    def test_with_same_type2(self):
        List = self._makeOne('List')
        Cons = List('Cons', 'head tail')
        Nil = List('Nil', '')

        self.assertEqual(Nil(), Nil())
