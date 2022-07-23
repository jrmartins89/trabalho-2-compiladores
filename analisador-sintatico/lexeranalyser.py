from sly import Lexer


class LexerAnalyser(Lexer):
    # Conjunto de tokens. Sempre é necessário.
    tokens = {DEF_IDENT,
              INT_IDENT,
              FLOAT_IDENT,
              STRING_IDENT,
              INT_CONSTANT,
              FLOAT_CONSTANT,
              STRING_CONSTANT,
              NULL,
              LPAREN,
              RPAREN,
              PLUS,
              MINUS,
              TIMES,
              DIVIDE,
              MOD,
              BREAK,
              PRINT,
              READ,
              LSQBRACKET,
              RSQBRACKET,
              LCBRACKET,
              RCBRACKET,
              RETURN,
              IF,
              ELSE,
              NEW,
              SEMICOLON,
              LESSTHAN,
              GREATERTHAN,
              LESSOREQUAL,
              GREATEROREQUAL,
              EQUALTO,
              DIFFERENTTHAN}

    # String que contém os caracteres ignorados entre os tokens
    ignore = ' \t'

    # Expressoes regulares para os tokens
    DEF = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'


if __name__ == '__main__':
    data = 'x = 3 + 42 * (s - t)'
    lexer = LexerAnalyser()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
