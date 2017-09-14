import re
from copy import deepcopy

import parsing
from complcated_errors import find_complicated_errors
from parsing import \
    check_and_parse_lexeme_and_exponent_pair as parse
from parsing import swap
from trivial_errors import find_trivival_errors


class Polynomial:
    """
    Class represents polynomial as a list of monomials.
    """
    def __init__(self, string) -> None:
        """
        Create a Polynomial instance using mathematical expression.
        """
        self.monomials = []
        if string is not None:
            if not isinstance(string, str):
                raise TypeError('Input must be string instance.')
            errorCheckMethods = [find_trivival_errors, find_complicated_errors]
            for method in errorCheckMethods:
                errorMessage = method(string)
                if errorMessage is not None:
                    if 'function' in errorMessage:
                        raise ValueError(errorMessage)
                    raise SyntaxError(errorMessage)
            string = parsing.normalize_expression(string)
            result = parse_composition(string)
            if isinstance(result, Monomial):
                self.monomials = [result]
            else:
                self.monomials = result.monomials

    def find_monomial(self, item) -> int:
        """
        Returns an index of item in list of monomials
        or -1 if this monomials is not in this list.
        """
        for index in range(len(self.monomials)):
            if self.monomials[index] == item:
                return index
        return -1

    def is_sub_polynomial(self, other, epsilon: float) -> bool:
        if not isinstance(other, Polynomial):
            raise TypeError('Only polynomial can be sub for polynomial.')
        for monomial in self.monomials:
            if monomial.coefficient != 0:
                monomialIndex = other.find_monomial(monomial)
                if monomialIndex == -1:
                    return False
                otherMonomial = other.monomials[monomialIndex]
                difference = otherMonomial.coefficient - monomial.coefficient
                if abs(difference) > epsilon:
                    return False
        return True

    def compare_by_epsilon(self, other, epsilon: float) -> bool:
        if not isinstance(other, Polynomial):
            raise TypeError('Polynomial can be compared only to polynomial.')
        return self.is_sub_polynomial(other, epsilon)\
            and other.is_sub_polynomial(self, epsilon)

    def __eq__(self, other) -> bool:
        return self.compare_by_epsilon(other, 0)

    def __add__(self, other):
        new = deepcopy(self)
        if isinstance(other, Monomial):
            monomialIndex = self.find_monomial(other)
            if monomialIndex == -1:
                new.monomials.append(other)
            else:
                new.monomials[monomialIndex] += other
        elif isinstance(other, Polynomial):
            for monomial in other.monomials:
                new += monomial
        else:
            raise TypeError(
                'Only monomial or polynomial can be added to polynomial.')
        return new

    def __mul__(self, other):
        if isinstance(other, Monomial) or isinstance(other, Polynomial):
            summary = Polynomial(None)
            for monomial in self.monomials:
                summary += (monomial * other)
            return summary
        else:
            raise TypeError(
                'Polynomial can be multiplied only by polynomial or monomial.')


class Monomial:
    def __init__(self, string: str):
        self.coefficient = None
        self.variables = None
        if string is not None:
            string = re.sub('[a-ik-z]', '(\g<0>)', string)
            lexemes = parsing.cut_composition_lexemes(string)
            coefficient = 1
            variables = {}
            message = 'Error in monomial {0}.'.format(swap(string, 'i', 'j'))

            for lexeme in lexemes:
                exponent = lexemes[lexeme]
                if lexeme in ['+', '-']:
                    lexeme += '1'
                try:
                    evaluatedLexeme, evaluatedExponent = parse(lexeme,
                                                               exponent)
                except ValueError as exception:
                    raise ValueError('{0} {1}'.format(message, str(exception)))
                except SyntaxError as exception:
                    raise SyntaxError(
                        '{0} {1}'.format(message, str(exception)))
                if not isinstance(evaluatedLexeme, str):
                    coefficient *= evaluatedLexeme
                elif evaluatedLexeme in variables:
                    variables[evaluatedLexeme] += evaluatedExponent
                else:
                    variables[evaluatedLexeme] = evaluatedExponent

            self.coefficient = coefficient
            self.variables = variables
            if self.coefficient == 0.0:
                self.variables = {}

    def __eq__(self, other) -> bool:
        # Two monomials are equal if their variable part are equals
        # Only keys (strs) and values (ints) will be compared.
        if not isinstance(other, Monomial):
            raise TypeError('Monomial can be compared only with monomial.')
        return other.variables == self.variables

    def __add__(self, other):
        if isinstance(other, Monomial):
            if other == self:
                new = deepcopy(self)
                new.coefficient += other.coefficient
                if new.coefficient == 0.0:
                    return Monomial('0')
                return new
            summary = Polynomial(None)
            summary.monomials = [self, other]
            return summary
        if isinstance(other, Polynomial):
            return other + self
        raise TypeError(
            'Monomial can be added only to monomial or polynomial.')

    def __mul__(self, other):
        if isinstance(other, Monomial):
            new = deepcopy(self)
            new.coefficient *= other.coefficient
            if new.coefficient == 0.0:
                return Monomial('0')
            for variable in other.variables:
                if variable in self.variables:
                    new.variables[variable] += other.variables[variable]
                else:
                    new.variables[variable] = other.variables[variable]
            return new
        elif isinstance(other, Polynomial):
            return other * self
        raise TypeError(
            'Monomial can be multiplied only by monomial or polynomial.')


def parse_composition(string: str):
    if parsing.check_monomial(string):
        return Monomial(string)
    if parsing.check_sum(string):
        return parse_sum(string)
    lexemes = parsing.cut_composition_lexemes(string)
    composition = None

    for lexeme in lexemes:
        exponent = lexemes[lexeme]
        message = 'Error in lexeme: {0}.'.format(swap(string, 'i', 'j'))
        try:
            evaluatedLexeme, evaluatedExponent = \
                parse(lexeme, exponent)
        except ValueError as exception:
            if str(exception)[0:5] != 'Error':
                raise ValueError('{0} {1}'.format(message, str(exception)))
            raise exception
        except SyntaxError as exception:
            if str(exception)[0:5] != 'Error':
                raise SyntaxError('{0} {1}'.format(message, str(exception)))
            raise exception
        # Since this moment we have non-arithmetical
        # lexeme and natural exponent.
        if not isinstance(evaluatedLexeme, str):
            evaluatedLexeme = str(evaluatedLexeme)
        if parsing.check_monomial(evaluatedLexeme):
            evaluatedLexeme = compose(
                Monomial(evaluatedLexeme), evaluatedExponent)
        else:
            evaluatedLexeme = compose(
                parse_sum(evaluatedLexeme), evaluatedExponent)
        if composition is None:
            composition = evaluatedLexeme
        else:
            composition *= evaluatedLexeme

    return composition


def compose(lexeme, exponent: int):
    if exponent >= 2:
        startLexeme = deepcopy(lexeme)
        for counter in range(exponent - 1):
            lexeme *= startLexeme
    return lexeme


def parse_sum(string: str):
    if not parsing.check_sum(string):
        return parse_composition(string)
    lexemes = parsing.cut_sum_lexemes(string)
    summary = None

    for lexeme in lexemes:
        if parsing.check_monomial(lexeme):
            evaluated = Monomial(lexeme)
        else:
            evaluated = parse_composition(lexeme)
        if summary is None:
            summary = evaluated
        else:
            summary += evaluated
    return summary
