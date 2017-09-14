import re
from math import trunc

from parsing import evaluate
from parsing import normalize_expression


def find_corresponding_bracket(string: str, index: int) -> int:
    """
    Find the position of the
    nearest corresponding bracket
    in string from the position of
    opening or closing bracket.
    """
    openingBracket = string[index] == '('
    bracketBalance = 0
    for pointer in (
            range(index + 1, len(string), 1) if openingBracket
            else range(index - 1, -1, -1)):
        subSymbol = string[pointer]
        nearestNotSpace = pointer
        for nearestNotSpace in range(pointer, len(string)):
            if string[nearestNotSpace] != ' ':
                break
        nextIsRaise =\
            (nearestNotSpace < len(string) - 1 and
             string[nearestNotSpace + 1] == '^') or\
            (nearestNotSpace < len(string) - 2 and
             string[nearestNotSpace + 1:nearestNotSpace + 3] == '**')
        if bracketBalance == 0 and\
           (subSymbol == (')' if openingBracket else '(')) and\
           (not nextIsRaise or not openingBracket):
            return pointer
        if subSymbol == ')':
            bracketBalance -= 1
        elif subSymbol == '(':
            bracketBalance += 1
    return pointer


def check_arithmetic(string: str) -> bool:
    """
    Checks if the expression doesn't contain variables.
    "i" is not a variable, it is an imaginary unit.
    """
    return len(re.findall('[a-hj-z]', string)) == 0


def find_operand_border(string: str, index: int, left: bool) -> int:
    """
    Finds the operator's left operand start or right operand end.
    """
    nearestSymbol = ' '
    nearestIndex = 0 if left else len(string) - 1
    for position in range(index - 1, -1, -1) if left\
            else range(index + 1, len(string), 1):
        nearestSymbol = string[position]
        if nearestSymbol != ' ':
            nearestIndex = position
            break
    if nearestSymbol == ')' if left else nearestSymbol == '(':
        return find_corresponding_bracket(string, nearestIndex)
    elif not check_arithmetic(nearestSymbol):
        return nearestIndex
    else:
        for position in (
                range(nearestIndex, -1, -1) if left
                else range(nearestIndex, len(string), 1)):
            if re.match('[0-9i. ]', string[position]) is None:
                return position + (1 if left else -1)
    return 0 if left else len(string) - 1


def indicate_borders_and_operands(string: str, operator) -> tuple:
    left_border = find_operand_border(string, operator.start(), True)
    right_border = find_operand_border(string, operator.end() - 1, False) + 1
    return (left_border, right_border,
            string[left_border:operator.start()],
            string[operator.end():right_border])


def iterate_operators(regular_expression: str):
    """
    Decorator for check error methods in this file.
    """
    def decorator(func):
        def wrapped(string: str) -> tuple:
            for operator in re.finditer(regular_expression, string):
                left_border, right_border, left_operand, right_operand = \
                    indicate_borders_and_operands(string, operator)
                message = func(string, right_operand, left_operand)
                if message is not None:
                    return message,\
                           string[left_border:right_border], operator.start()
        return wrapped
    return decorator


@iterate_operators(r'[/:]')
def check_division_error(
        string: str, right_operand: str = None,
        left_operand: str = None) -> str:
    """
    Checks if division operator in current position is incorrect.
    """
    if not check_arithmetic(right_operand):
        return 'Rational function found'
    else:
        try:
            denominator = evaluate(normalize_expression(right_operand))
            if abs(denominator) < 10**-10:
                return 'Division by zero'
        except SyntaxError:
            pass


@iterate_operators(r'(\^|\*{2})')
def check_raise_error(
        string: str, right_operand: str = None,
        left_operand: str = None) -> str:
    """
    Checks if raise operator in current position is incorrect.
    """
    if not check_arithmetic(right_operand):
        return 'Exponent function'\
            if check_arithmetic(left_operand)\
            else 'Power and exponent function'
    elif not check_arithmetic(left_operand):
        try:
            exponent = evaluate(normalize_expression(right_operand))
            if isinstance(exponent, complex):
                if abs(exponent.imag) < 10**-15:
                    exponent = exponent.real
                else:
                    return 'Complex exponent function'
            if isinstance(exponent, float):
                if abs(exponent - trunc(exponent)) < 10**-15:
                    exponent = round(exponent)
                else:
                    return 'Irrational function'
            if exponent < 0:
                return 'Rational function'
        except SyntaxError:
            pass
    else:
        try:
            foundation = evaluate(normalize_expression(left_operand))
            exponent = evaluate(normalize_expression(right_operand))
            if abs(foundation) < 10**-15 and exponent < 0:
                return 'Division by zero'
        except SyntaxError:
            pass


def find_complicated_errors(string: str) -> str:
    for method in [check_division_error, check_raise_error]:
        result = method(string)
        if result is not None:
            return '{0} found: {1} at {2} position.'.format(*result)
