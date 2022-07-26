from lexeranalyser import GCCLexer
from gccparser import GCCParser

if __name__ == '__main__':
    data = 'x = 3 + 42 * (s - t)'
    lexer = GCCLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))

    parser = GCCParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break

