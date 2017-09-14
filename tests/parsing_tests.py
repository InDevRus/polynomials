#!/usr/bin/python3
import unittest
import parsing


class MathExpressionTests(unittest.TestCase):
    def test_composition_lexemes(self):
        expressions = {('4xy3x^3y4x^5y/(3-5)(x+5y-x^2)' +
                       '^2.1(x+y)^(4+x(4x)-e)(xy)easy^3x/43'):
                           {'4xy3x^3y4x^5y': '1',
                            '3-5': '-(1)',
                            'x+5y-x^2': '2.1',
                            'x+y': '(4+x(4x)-e)',
                            'xy': '1', 'easy^3x/43': '1'},
                       '6xy*3/(x-y)(x-5)y^2*(z-2)':
                           {'6xy*3': '1', 'x-y': '-(1)',
                            'x-5': '1', 'y^2': '1', 'z-2': '1'}
                       }
        for expression in expressions:
            self.assertEqual(expressions[expression],
                             parsing.cut_composition_lexemes(
                                 expression))

    def test_sum_lexemes(self):
        expressions = {'3+x+x^2-3x^2+(x)-x^3-(x+2)^2+x-6-(x-3)^3':
                       ['3', 'x', 'x^2', '-3x^2', '(x)',
                        '-x^3', '-(x+2)^2', 'x', '-6', '-(x-3)^3'],
                       '-(x)^2+x^4-x': ['-(x)^2', 'x^4', '-x']}
        for expression in expressions:
            self.assertEqual(expressions[expression],
                             parsing.cut_sum_lexemes(expression))

    def test_check_sum(self):
        sums = ['3+(x-3)', '0*(x-2)(x+3)^3-3']
        compositions = ['6.59(x+3)', '4', '(x/(x+3)(x-8)+1)*(y)^32']
        for expression in sums:
            self.assertTrue(parsing.check_sum(expression))
        for expression in compositions:
            self.assertFalse(parsing.check_sum(expression))

    def test_check_arithmetic_expression(self):
        arithmeticExpressions = ['32', '2^(3+j)-j', 'j^j']
        nonArithmeticExpressions = ['3+x', '7^j+j-j+j^x']
        for expression in arithmeticExpressions:
            self.assertTrue(
                parsing.check_arithmetic(
                    expression))
        for expression in nonArithmeticExpressions:
            self.assertFalse(
                parsing.check_arithmetic(
                    expression))

    def test_check_monomial_expression(self):
        monomials = ['3(3+34^j)xy', 'a/(6+j)(6-j)/b', '3']
        nonMonomials = ['3*x*y/z(j+1)-1', '26*(6^1.5)/x*(j+(x))']
        for expression in monomials:
            self.assertTrue(parsing.check_monomial(expression))
        for expression in nonMonomials:
            self.assertFalse(parsing.check_monomial(expression))

    def test_find_corresponding_bracket(self):
        sets = [('3+()', 3, 2), ('3+()', 2, 3), ('x+y-(e^2**3)+(4)', 4, 11),
                ('x+y-(e^2**3)+(4)', 11, 4), ('x+y-(e^2**3)+(4)', 13, 15),
                ('x+y-(e^2**3)+(4)', 15, 13), ('a(b((x)3))+9()', 1, 9),
                ('a(b((x)3))+9()', 6, 4), ('a(b((x)3))+9()', 3, 8),
                ('(abc)', 0, 4), ('(abc)', 4, 0)]
        for data in sets:
            self.assertEqual(
                parsing.find_corresponding_bracket(data[0], data[1]), data[2])

if __name__ == '__main__':
    unittest.main()
