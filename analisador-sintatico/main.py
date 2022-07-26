from lexeranalyser import GCCLexer

if __name__ == '__main__':
    data = 'x = 3 + 42 * (s - t)'
    lexer = GCCLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))

