import unittest
import pathmagic
from math_methods.complcated_errors import check_division_error
from math_methods.complcated_errors import check_raise_error
from math_methods.complcated_errors import find_operand_border


class ComplicatedErrorCheckTests(unittest.TestCase):
    def correct_assertion(self, assert_func, data: list):
        for item in data:
            self.assertIsNone(assert_func(item))

    def incorrect_assertion(self, assert_func, sets: list):
        for data in sets:
            result = assert_func(data[0])
            self.assertEqual(result[1], data[1])
            self.assertEqual(result[2], data[2])

    def test_correct_raising(self):
        self.correct_assertion(check_raise_error,
                               ['3x**2', 'x+y+x**3+x**2', '4**(4/0)'])

    def test_incorrect_raising(self):
        self.incorrect_assertion(check_raise_error,
                                 [(' 0 ** (3-4)', ' 0 ** (3-4)', 3),
                                  ('2^(3)**(x)', '2^(3)**(x)', 1),
                                  ('x**x', 'x**x', 1),
                                  ('x**a', 'x**a', 1),
                                  ('x^ax', 'x^a', 1),
                                  ('3+ x    ** (axy)', 'x    ** (axy)', 8),
                                  ('x^i', 'x^i', 1),
                                  (' b**(2^i)', 'b**(2^i)', 2),
                                  ('x**(2-5)', 'x**(2-5)', 1),
                                  ('(x)**(2)^(i)', '(x)**(2)^(i)', 3),
                                  ('4+6-x**(7/8)', 'x**(7/8)', 5),
                                  ('x**(0**(-2))', '0**(-2)', 5)
                                  ])

    def test_correct_division(self):
        self.correct_assertion(check_division_error,
                               ['2/2', '23/ix',
                                '2**i+i-2', 'i**i',
                                'i+i-i**(2i)', 'x**2**i'])

    def test_incorrect_division(self):
        self. \
            incorrect_assertion(check_division_error,
                                [(' 3:(x y)', ' 3:(x y)', 2),
                                 ('1/( x + y )', '1/( x + y )', 1),
                                 ('4i/x', '4i/x', 2),
                                 ('14j/x', 'j/x', 3),
                                 ('142+4.25/0.0-x', '4.25/0.0', 8),
                                 ('0+0/5-(3+2)/(1.5+2.5-4)',
                                  '(3+2)/(1.5+2.5-4)', 11),
                                 ('1/x', '1/x', 1), ('5/(x)', '5/(x)', 1),
                                 ('(x)/(0)', '(x)/(0)', 3),
                                 ('3/(2/0)', '2/0', 4)])

    def test_find_left_operand_start(self):
        sets = [('13/4', 2, 0), ('x*13/4', 4, 2), ('x+ 3 4 /5xy', 7, 2),
                ('+ (3 )   /(a)', 9, 2), (' 3:3', 2, 0)]
        for data in sets:
            self.assertEqual(find_operand_border(data[0],
                                                 data[1],
                                                 True), data[2])

    def test_find_right_operand_end(self):
        sets = [('x+ 3 4 /5xy', 7, 8), ('13/4', 2, 3), ('x*13/4', 4, 5),
                ('+ (3 )   /(a)', 9, 12), ('1/( x + y )', 1, 10)]
        for data in sets:
            self.assertEqual(find_operand_border(data[0],
                                                 data[1],
                                                 False), data[2])


if __name__ == '__main__':
    unittest.main()
