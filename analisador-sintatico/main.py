from lexeranalyser import GCCLexer

if __name__ == '__main__':
    lexer = GCCLexer()
    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
