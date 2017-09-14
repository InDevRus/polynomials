import argparse
from sys import stdin, stderr

from polynomial import Polynomial

# Arguments definition.
parser = argparse.ArgumentParser(
    description='Parses expressions and checks if entered expressions are' +
                ' polynomials and they are equals by epsilon.')
parser.add_argument('first', nargs='?', help='first expression')
parser.add_argument('second', nargs='?', help='second expression')
compareGroup = parser.add_mutually_exclusive_group()
compareGroup.add_argument(
    '-e', '--epsilon', help='change default epsilon',
    type=float, default=10**(-6), metavar='eps')
compareGroup.add_argument(
    '-d', '--decimal', help='change default epsilon by formula in readme',
    type=int, metavar='n'
)
compareGroup.add_argument(
    '-m', '--match', help='set to compare number by match',
    action='store_true')
parser.add_argument(
    '-s', '--specific',
    help='show specific information about errors in polynomials',
    action='store_true')
parser.add_argument('-f', '--file', help='an expressions file link',
                    metavar='file')
args = parser.parse_args()

expressionPair = []

if args.first is not None:
    expressionPair.append(args.first)
if args.second is not None:
    expressionPair.append(args.second)

if len(expressionPair) < 2 and args.file is not None:
    link = args.file
    with open(link) as file:
        for line in file:
            cut = line.replace('\n', '')
            if cut != '':
                expressionPair.append(cut)
            if len(expressionPair) == 2:
                break

if len(expressionPair) < 2:
    for line in stdin:
        cut = line.replace('\n', '')
        if cut != '':
            expressionPair.append(cut)
        if len(expressionPair) == 2:
            break

if len(expressionPair) < 2:
    if len(expressionPair) == 0:
        print('There is no expressions to parse and compare.\n', file=stderr)
    elif len(expressionPair) == 1:
        print(
            'There is no second expression to parse and compare to gained.\n',
            file=stderr)
    exit(1)


def print_error_message(number: int):
    if number == 1:
        print('Error in first expression.\n', file=stderr)
    elif number == 2:
        print('Error in second expression.\n', file=stderr)


try:
    first = Polynomial(expressionPair[0])
except SyntaxError as exception:
    print_error_message(1)
    if args.specific:
        print(str(exception), file=stderr)
    exit(3)
except ValueError as exception:
    print_error_message(1)
    if args.specific:
        print(str(exception), file=stderr)
    exit(4)

try:
    second = Polynomial(expressionPair[1])
except SyntaxError as exception:
    print_error_message(2)
    if args.specific:
        print(str(exception), file=stderr)
    exit(5)
except ValueError as exception:
    print_error_message(2)
    if args.specific:
        print(str(exception), file=stderr)
    exit(6)

if args.match:
    equals = first == second
else:
    if args.decimal is not None:
        epsilon = 10**(-args.decimal)
    else:
        epsilon = args.epsilon
    equals = first.compare_by_epsilon(second, epsilon)

if equals:
    print('Polynomials are equal.')
    exit(0)
else:
    print('Polynomials are not equal.')
    exit(1)
