# -*- coding:utf-8 -*-
import unittest

class VariantTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from miniadt import ADTTypeProvider
        cls.Result = ADTTypeProvider("Result")
        cls.Failure = cls.Result("Failure", "code message")
        cls.Success = cls.Result("Success", "value")

    def _getTarget(self):
        from miniadt import dispatchmethod
        @self.Result.match
        class Match0(object):
            @dispatchmethod
            def Failure(code, message):
                return ["oops", code, message]

            @dispatchmethod
            def Success(value):
                return ["ok", value]
        return Match0


    def test_comprehesive(self):
        self.assertTrue(self.Result.is_comprehensive(["Failure", "Success"]))

    def test_comprehesive__include_missing_type(self):
        self.assertFalse(self.Result.is_comprehensive(["Failure", "Success", "Another"]))

    def test_success(self):
        target = self._getTarget()
        result = target(self.Success('{"result": "good"}'))
        self.assertEqual(result, ["ok", '{"result": "good"}'])

    def test_failure(self):
        target = self._getTarget()
        result = target(self.Failure(404, "not found"))
        self.assertEqual(result, ["oops", 404, "not found"])

    def test_validation__failure(self):
        from miniadt import ADTTypeProvider, NotComprehensive

        target = self._getTarget()

        Another = ADTTypeProvider("Another")
        Another("Item", "name value")

        with self.assertRaisesRegexp(NotComprehensive, "Item"):
            Another.validation(target)

    def test_validation__failure2(self):
        from miniadt import dispatchmethod, NotComprehensive

        class Match0(object):
            @dispatchmethod
            def Failure(code, message):
                return ["oops", code, message]

            @dispatchmethod
            def Success(code, message): #xxx: arguments are wrong
                return ["ok", code, message]

        with self.assertRaisesRegexp(NotComprehensive, "'code', 'message'"):
            self.Result.match(Match0)
