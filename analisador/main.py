from gcclexer import GCCLexer
from gccparser import GCCParser

if __name__ == '__main__':
    data = 'def func1 (int A, int B){' \
           'int SM [2];' \
           'SM [0] = A + B;' \
           'SM [1] = B * C;' \
           'return ;' \
           '}' \
           'def principal ()' \
           '{' \
           'int C;' \
           'int D;' \
           'int R;' \
           'C = 4;' \
           'D = 5;' \
           'R = func1 (C, D);' \
           'return ;' \
           '}'
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

