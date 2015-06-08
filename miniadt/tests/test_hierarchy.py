# -*- coding:utf-8 -*-
import unittest


class HierarchyTests(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from miniadt import ADTTypeProvider
        return ADTTypeProvider(*args, **kwargs)

    def test_adttype_is_subclass_of_adttype(self):
        from miniadt import ADTType
        provider = self._makeOne("C")
        T = provider("T", "")
        self.assertTrue(issubclass(T, ADTType))

    def test_adttype_is_subclass_of_base(self):
        provider = self._makeOne("C")
        T0 = provider("T0", "")
        T1 = provider("T1", "")
        self.assertTrue(issubclass(T0, provider.base))
        self.assertTrue(issubclass(T1, provider.base))

    def test_adttype_is_not_subclass_of_another_base(self):
        provider = self._makeOne("C0")
        another = self._makeOne("C1")
        T = provider("T", "")
        self.assertTrue(issubclass(T, provider.base))
        self.assertFalse(issubclass(T, another.base))

    def test_single_dispatch(self):
        from singledispatch import singledispatch
        provider = self._makeOne("C")
        T0 = provider("T0", "")
        T1 = provider("T1", "")

        @singledispatch
        def generic(x):
            return "g"

        @generic.register(provider.base)
        def c(x):
            return "c"

        @generic.register(T0)
        def t0(x):
            return "t0"

        self.assertEqual(generic(object()), "g")
        self.assertEqual(generic(T1()), "c")
        self.assertEqual(generic(T0()), "t0")
