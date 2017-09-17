import unittest
import pathmagic
from math_methods.trivial_errors import check_bracket_balance
from math_methods.trivial_errors import find_trivival_errors as check


class TrivialErrorCheckTests(unittest.TestCase):
    def assert_check_expressions(self, correct: list, incorrect: list):
        for number in correct:
            self.assertIsNone(check(number))
        for number in incorrect:
            self.assertIsNotNone(check(number))

    def test_incorrect_numbers(self):
        correctNumbers = ['1', '2.5', '100+5,5']
        incorrectNumbers = ['3.4.', '.4', '+4.', '@.4', '8.+6', '1.4.',
                            '2.5.7.3', '0......', '0...']
        self.assert_check_expressions(correctNumbers, incorrectNumbers)

    def test_bracket_balance(self):
        correctExpressions = ['', '(())', 'x+(x)+((x)x)']
        noEnclosingBrackets = {'(': 0, '((((((())': 4,
                               '()()(())()(': 10, '(x)(x+2(x)': 3}
        noOpeningBrackets = {')': -1, ')(()': -1, 'x + ) - ( x ': -5}
        for expression in correctExpressions:
            self.assertIsNone(check_bracket_balance(expression))
        for expression in noEnclosingBrackets:
            result = check_bracket_balance(expression)
            self.assertIsInstance(result, int)
            self.assertEqual(result, noEnclosingBrackets[expression])
        for expression in noOpeningBrackets:
            result = check_bracket_balance(expression)
            self.assertIsInstance(result, int)
            self.assertEqual(result, noOpeningBrackets[expression])

    def test_incorrect_operators(self):
        correctOperators = ['+4556z-e', '45+x', '3.52-r*w^3', '-58', '(-6+5)',
                            '9*(+6)']
        incorrectOperators = ['+', '-', '4-*', '3+8*^4.6',
                              '-45z+2.5^3+', '3**', '(3**)', '2+()',
                              '()', '2()3**2', '3:', '0/']
        self.assert_check_expressions(correctOperators, incorrectOperators)

    def test_unexpected_symbols(self):
        correctExpressions = ['3+56gt', '3+6+c-z', '+d-z^5']
        incorrectExpressions = ['@xt', '$', '5+5%3',
                                '4+form!', 'violin2@22222']
        self.assert_check_expressions(correctExpressions, incorrectExpressions)


if __name__ == '__main__':
    unittest.main()
