from lexeranalyser import LexerAnalyser
from parser import Parser

if __name__ == "__main__":
    lexer = LexerAnalyser()
    parser = Parser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
