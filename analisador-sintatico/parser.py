from sly import Parser

class Parser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens