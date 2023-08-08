from pyparsing import QuotedString, Word, CaselessKeyword, Literal, Suppress, OneOrMore, Group
from pyparsing import Forward, ZeroOrMore, SkipTo
from pyparsing import nums, alphanums, Optional, alphas

registry = '%' + Word(alphanums)

header = SkipTo('.text:')

store_in_registry = '(' + registry + ')'

memAddr = '*' + Word(alphanums) + store_in_registry
literal = '$' + Word(alphanums)

comm = Word(alphas)
arg = Word(alphas) | registry

comment = '#' + Word(alphanums)

memcomm = comm + memAddr
operand = comm + OneOrMore(arg + ZeroOrMore(','))
divisor = '|'

inst = operand | memcomm | comment | divisor

def load_binary():
    with open('ls_short.s', 'r', encoding='utf-8') as f:
        binary = f.read()

    binary = binary.replace('\t', '')
    binary = binary.split('\n')

    return binary

def main():
    loaded_binary = load_binary()
    print(loaded_binary)

if __name__ == "__main__":
    main()
