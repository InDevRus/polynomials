#!/usr/bin/python3
import re
from math import trunc


def cut_composition_lexemes(string: str) -> dict:
    """
    Returns a dict of lexemes with
    foundation of degree as keys
    and exponent as corresponding value.
    """
    index = 0
    lastLexeme = 0
    wasDivision = False
    lexemesDict = {}
    length = len(string)

    while index < length:
        symbol = string[index]
        if symbol == '/':
            wasDivision = True
        elif symbol == '(' and (index == 0 or string[index - 1] != '^'):
            previousToken = string[lastLexeme:index]
            if previousToken != '':
                if index != 0 and string[index - 1] in '*/':
                    previousToken = previousToken[:-1]
                update_dict_key(lexemesDict, previousToken, '1')
            enclosingBracket = find_corresponding_bracket(string, index)
            token = string[index + 1:enclosingBracket]
            if enclosingBracket == length - 1\
                    or string[enclosingBracket + 1] != '^':
                exponent = '1'
                exponentEnd = enclosingBracket + 1
            else:
                exponentEnd = enclosingBracket + 2
                while True:
                    if string[exponentEnd] == '(':
                        exponentEnd = find_corresponding_bracket(
                            string, exponentEnd)
                        exponentEnd += 1
                    else:
                        while exponentEnd < length:
                            exponentSymbol = string[exponentEnd]
                            if not (exponentSymbol.isdigit() or
                                    exponentSymbol == '.') and\
                                    exponentEnd != enclosingBracket + 2:
                                break
                            exponentEnd += 1
                    if exponentEnd >= length - 1 or string[exponentEnd] != '^':
                        break
                    exponentEnd += 1
                exponent = string[enclosingBracket + 2:exponentEnd]
            if wasDivision:
                exponent = '-(' + exponent + ')'
                wasDivision = False
            update_dict_key(lexemesDict, token, exponent)
            lastLexeme = exponentEnd
            index = exponentEnd - 1
        else:
            wasDivision = False
        index += 1
    previousToken = string[lastLexeme:index]
    update_dict_key(lexemesDict, previousToken, '1')
    lexemesDict.pop('', None)
    return lexemesDict


def update_dict_key(dictionary: dict, key: str, value: str) -> None:
    """
    If key is in dictionary, value
    will be added to existing value,
    else value will be assigned to key.
    """
    if key not in dictionary:
        dictionary[key] = value
    else:
        dictionary[key] += '+' + value


def normalize_expression(string: str) -> str:
    string = string.replace(' ', '').replace(',', '.') \
        .replace('**', '^').replace(':', '/')
    # Complex unit replacement.
    string = swap(string, 'i', 'j')
    # Deleting unnecessary asterisks
    # (asterisks needed only to separate numbers and imaginary units)
    string = re.sub('([^\d])\*', '\g<1>', string)
    string = re.sub('\*([^\d])', '\g<1>', string)
    # Wrapping numbers and variables before and after exponent into brackets
    string = re.sub('([\d.]+|[a-z])\^', '(\g<1>)^', string)
    string = re.sub('\^([\d.]+|[a-z])', '^(\g<1>)', string)
    return string


def cut_sum_lexemes(string: str) -> list:
    """
    Returns a list of sum lexemes in a list.
    """
    index = 0
    lexemeList = []
    lastLexeme = 0
    while index < len(string):
        symbol = string[index]
        if symbol in '+-':
            token = string[lastLexeme:index]
            if token != '':
                lexemeList.append(token)
            lastLexeme = index
            if symbol == '+':
                lastLexeme += 1
        elif symbol == '(':
            index = find_corresponding_bracket(
                string, index)
        index += 1
    token = string[lastLexeme:index]
    if token != '':
        lexemeList.append(token)
    return lexemeList


def check_sum(string: str) -> bool:
    """
    Checks if the string has + or - operators
    outside of the brackets.
    """
    bracketBalance = 0
    for index in range(len(string)):
        symbol = string[index]
        if symbol == '(':
            bracketBalance += 1
        elif symbol == ')':
            bracketBalance -= 1
        elif symbol in '+-' and bracketBalance == 0 and index > 0:
            return True
    return False


def check_arithmetic(string: str) -> bool:
    """
    Checks if the expression doesn't contain variables.
    "j" is not a variable, it is an imaginary unit.
    """
    return re.search('[a-ik-z]', string) is None


def check_monomial(string: str) -> bool:
    """
    Checks if the expression is monomial, where
    monomial is the mathematical expression that
    does not contain variables and "+", "-"
    outside of the brackets.
    Possible exception: "+" or '-' at the beginning.
    """
    bracketBalance = 0
    for symbol in string:
        if symbol == '(':
            bracketBalance += 1
        elif symbol == ')':
            bracketBalance -= 1
        elif symbol.isalpha() and symbol != 'j' and bracketBalance > 0:
            return False
    return not check_sum(string)


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
        if bracketBalance == 0 and subSymbol == (')' if openingBracket
                                                 else '('):
            return pointer
        if subSymbol == ')':
            bracketBalance -= 1
        elif subSymbol == '(':
            bracketBalance += 1


def swap(string: str, first: str, second: str) -> str:
    """
    Returns a string with first character replaced
    with second and second character replaced with first.
    """
    result = ''
    for symbol in string:
        if symbol == first:
            result += second
        elif symbol == second:
            result += first
        else:
            result += symbol
    return result


def evaluate(expression: str):
    """
    Evaluates given expression.
    """
    original = expression
    # Replacing caret with double asterisk.
    expression = expression.replace('^', '**')
    # Separating double imaginary unit with asterisk.
    expression = expression.replace('jj', 'j*j').replace('jj', 'j*j')
    # Adding coefficient before imaginary unit.
    expression = re.sub('(\D|^)j', '\g<1>1j', expression)
    # Adding asterisk before opening brackets
    # if number, imaginary unit or enclosing
    # bracket was before opening one.
    expression = re.sub('([\dj)])\(', '\g<1>*(', expression)
    try:
        return eval(expression)
    except (SyntaxError, ZeroDivisionError):
        raise SyntaxError(swap(original, 'i', 'j'))


def check_and_parse_lexeme_and_exponent_pair(lexeme: str,
                                             exponent: str) -> tuple:
    evaluatedLexeme = lexeme
    if evaluatedLexeme in ['+', '-']:
        evaluatedLexeme += '1'
    if evaluatedLexeme[0] == '/':
        evaluatedLexeme = evaluatedLexeme[1:]
        exponent = '-({0})'.format(exponent)
    # Checks if exponent have variables.
    if not check_arithmetic(exponent):
        if not check_arithmetic(evaluatedLexeme):
            raise ValueError(
                generate_message('Power and exponent function',
                                 evaluatedLexeme, exponent))
        else:
            raise ValueError(
                generate_message(
                    'Exponent function', evaluatedLexeme, exponent))
    # If there is no exponent function,
    # we can evaluate exponent without any troubles.
    try:
        evaluatedExponent = evaluate(exponent)
    except SyntaxError as exception:
        raise SyntaxError(
            'Failed evaluating exponent: {0}.'.format(str(exception)))
    if check_arithmetic(evaluatedLexeme):
        try:
            return evaluate(evaluatedLexeme) ** evaluatedExponent, 1
        except SyntaxError as exception:
            raise SyntaxError(
                'Failed evaluating lexeme: {0}.'.format(str(exception)))
        except ZeroDivisionError:
            raise SyntaxError(
                generate_message('Division by zero', lexeme,
                                 str(evaluatedExponent)))
    else:
        message = None
        try:
            if isinstance(evaluatedExponent, complex):
                if abs(evaluatedExponent.imag) < 10**-15:
                    evaluatedExponent = evaluatedExponent.real
                else:
                    message = generate_message('Complex exponent function',
                                               lexeme,
                                               str(evaluatedExponent)[1:-1])
            if isinstance(evaluatedExponent, float):
                if abs(evaluatedExponent - trunc(evaluatedExponent)) < 10**-15:
                    evaluatedExponent = round(evaluatedExponent)
                else:
                    message = generate_message('Irrational function',
                                               lexeme, str(evaluatedExponent))
            if evaluatedExponent < 0:
                message = generate_message('Rational function',
                                           lexeme, str(evaluatedExponent))
        finally:
            if message is not None:
                raise ValueError(message)
        if evaluatedExponent == 0:
            evaluatedLexeme = 1
            evaluatedExponent = 1

    return evaluatedLexeme, evaluatedExponent


def generate_message(message: str, lexeme: str, exponent: str) -> str:
    return('{0} found: {1} was raised to {2}.'
           .format(message, swap(lexeme, 'i', 'j'), swap(exponent, 'i', 'j')))
