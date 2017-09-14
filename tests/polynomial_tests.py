#!/usr/bin/python3
import unittest
from polynomial import Polynomial, Monomial
import itertools
import math


class MonomialInitializeTest(unittest.TestCase):
    def test_monomial_initialize(self):
        expressions = [('ab', 1, {'a': 1, 'b': 1}),
                       ('x^2y', 1, {'x': 2, 'y': 1}),
                       ('xyxx/(4+2+1+1)y', 0.125, {'x': 3, 'y': 2}),
                       ('xxxxxxxx2.000000000', 2, {'x': 8})]
        for expression in expressions:
            monomial = Monomial(expression[0])
            self.assertEqual(expression[1], monomial.coefficient)
            self.assertEqual(expression[2], monomial.variables)

    def test_incorrect_monomials(self):
        incorrectExpressions = ['2xy^x', '12*(2+1j)/2j/x',
                                '9x^3.3', 'a^(34+1j)']
        for expression in incorrectExpressions:
            with self.assertRaises(ValueError):
                Monomial(expression)


class MonomialOperations(unittest.TestCase):
    def apply_function(self, func, first: str,
                       second: str, coefficient,
                       variables: dict) -> None:
        result = func(Monomial(first), Monomial(second))
        self.assertEqual(result.coefficient, coefficient)
        self.assertEqual(result.variables, variables)

    def test_multiply_monomials(self):
        combinations = [('3', '2', 6, {}), ('x', 'x', 1, {'x': 2}),
                        ('xy3(2-1j)', 'xy/6', (1-0.5j), {'x': 2, 'y': 2}),
                        ('2.5jab', '100a^2b^5c', (0+250.0j),
                         {'a': 3, 'b': 6, 'c': 1}), ('xy', 'a/3b',
                                                     1/3, {'x': 1,
                                                           'y': 1,
                                                           'a': 1,
                                                           'b': 1})]
        for combination in combinations:
            self.apply_function(lambda x, y: x * y, *combination)
            self.apply_function(lambda x, y: y * x, *combination)

    def test_add_similar_monomials(self):
        combinations = [('0xy', '2.4^1.0', 2.4, {}),
                        ('3xy', '-5yx', -2, {'x': 1, 'y': 1}),
                        ('6x^2y^5x', '-20xyyxyyyx', -14, {'x': 3, 'y': 5}),
                        ('5jxy', '(3-5j)yx', 3, {'x': 1, 'y': 1}),
                        ('3xy', '(5-2^3)yx', 0, {})]
        for combination in combinations:
            self.apply_function(lambda x, y: x + y, *combination)


class PolynomialOperations(unittest.TestCase):
    def apply_function(self, func, first: str,
                       second: str, result: str) -> None:
        applied = func(Polynomial(first), Polynomial(second))
        self.assertEqual(Polynomial(result), applied)

    def check_equality_of_items_in_iterable(self, iterable) -> None:
        pairs = [pair for pair in
                 itertools.combinations_with_replacement(iterable, 2)]
        for pair in pairs:
            self.assertEqual(Polynomial(pair[0]), Polynomial(pair[1]))

    def test_equal_polynomials(self):
        chainsOfPolynomials = [['x**2+2', '2+3x+x**2-x*3'],
                               ['x^2+4x+4', 'x**2+2x+4+2(x)',
                                '(x+2)**2', '(x+2)(x+2)',
                                '(x-y)(x+y)+y**2+4+4(x)'],
                               ['(x+y)(x+z)(y+z)', '(y+z)(x+z)(x+y)',
                                '(x+y)*(xy+zy+z*x+z**2)',
                                '(x+y)xy+(x+y)zy+(zx)(x+y)+(z**2)(x+y)',
                                '(x**2y+xy**2+xyz+(y**2z)+' +
                                '(zx**2)+yxz+(z**2x)+yz**2)'],
                               ['(x+u+v)/2.0', 'u/2.0+x/2.0+4v/8.0'],
                               ['(3**2)', '3**2', '9']]
        for chain in chainsOfPolynomials:
            self.check_equality_of_items_in_iterable(chain)

    def test_different_polynomials(self):
        pairs = [('5x**2+3y**2', '5x**2+3y'),
                 ('3xy', '3.000000000000001xy'),
                 ('xy+xy', 'xy'),
                 ('1.01xy', 'xy'),
                 ('x**2', 'x^2+x'),
                 ('y**3', 'x+y^3')]
        for pair in pairs:
            self.assertNotEqual(Polynomial(pair[0]), Polynomial(pair[1]))

    def test_add_non_similar_monomials(self):
        combinations = [('8x**2y**2', '8xy', '8xy+8x^2y^2'),
                        ('x**2', '-y**2', '(x+y)(x-y)')]
        for combination in combinations:
            self.apply_function(lambda x, y: x + y, *combination)
            self.apply_function(lambda x, y: y + x, *combination)

    def test_add_polynomials(self):
        combinations = [('x**3-y^3', '3(y-x)xy', '(x-y)**3'),
                        ('xy+2xy', '-x', '-x+3x(y)')]
        for combination in combinations:
            self.apply_function(lambda x, y: x + y, *combination)
            self.apply_function(lambda x, y: y + x, *combination)

    def test_sequence_of_raise_operators(self):
        chainsOfPolynomials = [['(2+6**2)x**(2+4-6)**2', '38'],
                               ['((2+6**2)x)**(2+4-6)**2', '1',
                                '1**1**1**1**1**1'],
                               ['x**3^3', 'x^27',
                                'x**27', 'x**27**1**(2+4-6)'],
                               ['(x**2)^3', '(x**3)**2', 'x**6',
                                '(x**1)**6', '(x**1)**6**1']]
        for chain in chainsOfPolynomials:
            self.check_equality_of_items_in_iterable(chain)

    def test_imaginary_unit_after_raise_operator(self):
        chainsOfPolynomials = [['3**(16/5)**i', '3**3.2**i', '3**(3.2^i)'],
                               ['2**i + x', '2x + 2**(1i) - x',
                                '(1+1)**i + 0.0 +x']]
        for chain in chainsOfPolynomials:
            self.check_equality_of_items_in_iterable(chain)

    def test_short_multiplication_formulas(self):
        chains = [['(x+y)**1', '1', 'x+y'],
                  ['x+y', 'x+y', 'x**2+2xy+y**2'],
                  ['x-y', 'x-y', 'x**2-2xy+y**2'],
                  ['(x+y)**3', '1', 'x**3+3x**2y+3y**2x+y**3'],
                  ['(x-y)**3', '1', 'x**3-3x**2y+3y**2x-y**3'],
                  ['x**2+xy+y**2', 'x-y', 'x**3-y**3'],
                  ['x**2-xy+y**2', 'x+y', 'x**3+y**3'],
                  ['x+y+z', 'x+y+z', 'x**2+y**2+z**2+2xy+2xz+2yz'],
                  ['x-y-z', 'x-y-z', 'x**2+y**2+z**2-2xy-2xz+2yz']]
        for chain in chains:
            self.apply_function(lambda x, y: x * y, *chain)
            self.apply_function(lambda x, y: y * x, *chain)

    def test_compare_by_epsilon(self):
        toCompare = ['2.718281828', '2.7+1828/99990']
        for value in toCompare:
            first = Polynomial(str(math.e))
            second = Polynomial(value)
            self.assertTrue(first.compare_by_epsilon(second, 10**(-9)))
            self.assertFalse(first.compare_by_epsilon(second, 10**(-10)))

    def test_difficult_evaluating(self):
        chains = [['0*i + 3', '3+i * 0', '3'],
                  ['x**((1-i)(1+i))', 'x**2', 'x^2.0',
                   'x**1.9999999999999999999999999',
                   'x**(-2ii)', 'x**(1(2))', 'x**(-2i(1i))**(1)']]
        for chain in chains:
            self.check_equality_of_items_in_iterable(chain)

    def test_incorrect_expressions(self):
        incorrectExpressions = ['x + y**(3/0)', 'y/(3-3)']
        for expression in incorrectExpressions:
            with self.assertRaises(SyntaxError) as exception:
                Polynomial(expression)
                message = str(exception)
                self.assertIn('Failed evaluating', message)
        incorrectValues = ['1+x+y-x+y/x', '3-2+x**(1+4x)',
                           '3**(4+x)', 'x**1**1**2**3**(2+3-x)']
        for expression in incorrectValues:
            with self.assertRaises(ValueError) as exception:
                Polynomial(expression)
                message = str(exception)
                self.assertIn('Error in', message)

if __name__ == '__main__':
    unittest.main()
