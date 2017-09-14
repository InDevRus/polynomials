#!/usr/bin/python3
import re


# These functions checks mathematical expression, except the last one.
# Check tests for more information.
def find_incorrect_numbers(string: str):
    return re.finditer('((?:\D|^) *[.,][ \d]*|[ \d]*[.,] *(?:\D|$)' +
                       '|[\d ]*[.,][ \d]*[.,][\d ]*)', string)


def check_bracket_balance(string: str) -> int:
    bracketStack = []
    for index in range(len(string)):
        char = string[index]
        if char == '(':
            bracketStack.append(index)
        elif char == ')':
            if len(bracketStack) == 0:
                return -index - 1
            bracketStack.pop()
    if len(bracketStack) > 0:
        return bracketStack.pop()


def find_incorrect_operators(string: str):
    return re.finditer('(^ *[*:/^]|[+\-*:/^] *$|[+\-*:/^] *[+\-:/^]|[+\-:/^]' +
                       ' *[+\-*:/^]|[+\-*:/^] *\*{2}|\*{2} *[+\-*:/^]|' +
                       '\( *[*:/^]|[*:/^] *\)|\( *\))',
                       string)


def find_unexpected_symbols(string: str):
    return re.finditer('[^a-z+\-*:/^()\d., ]', string)


"""def find_trivial_exponent(string: str):
    return re.finditer('((?:\*{2}|\^) *(?:[a-hj-z]|\( *[a-hj-z ]+ *\)))',
                       string)


def find_trivial_complex_function(string: str):
    return re.finditer('(?:[a-hj-z]|\([a-hj-z ]+\)) *(\*{2}|\^) ' +
                       '*(?:i|\( *[\d.] *\*? *i\)) *(?!\*{2}|\^)', string)


def find_trivial_rational_function(string: str):
    return re.finditer('([/:] *(?:[a-hj-z]|\( *[a-hj-z]+ *\)))', string)"""


def find_trivival_errors(string: str) -> str:
    """
    Uses all the functions above to check
    mathematical expression and find errors.
    """
    balance = check_bracket_balance(string)
    if balance is not None:
        message = 'Unbalanced brackets: {0}.'
        if balance < 0:
            return message.format('no opening brackets for ' +
                                  'bracket at {0} position'.format(
                                      abs(balance) - 1))
        else:
            return message.format('no enclosing brackets for ' +
                                  'bracket at {0} position'.format(balance))
    methods = {find_incorrect_numbers: 'Incorrect numbers: {0}.',
               find_unexpected_symbols: 'Unexpected symbols: {0}.',
               find_incorrect_operators: 'Incorrect operator sequence: {0}.'}
    for method in methods:
        errorsIterable = method(string)
        message = ''
        for matchObject in errorsIterable:
            group = matchObject.group(0)
            start = matchObject.start()
            message += '{0} at {1} position, '.format(group, start)
        if message != '':
            return methods[method].format(message[:-2])
