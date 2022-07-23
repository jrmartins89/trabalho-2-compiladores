from sly import Lexer


class LexerAnalyser(Lexer):
    # Conjunto de tokens. Sempre é necessário.
    tokens = {DEF, IDENT, NUMBER, PLUS, MINUS, TIMES,
     DIVIDE, ASSIGN, LPAREN, RPAREN, LBRACE,
     RBRACE, LBRACKET, RBRACKET, INT, FLOAT, STRING,
     SEMICOL, BREAK, COL, READ, PRINT, RETURN, IF, ELSE, FOR, NEW,
     GT, LT, GE, LE, EQ, NOTEQ, REMAINDER, INT_CONSTANT, FLOAT_CONSTANT, STRING_CONSTANT, NULL}

    # reserved words
    DEF = r'\bdef\b'
    INT = r'\bint\b'
    FLOAT = r'\bfloat\b'
    STRING = r'\bstring\b'
    BREAK = r'\bbreak\b'
    READ = r'\bread\b'
    PRINT = r'\bprint\b'
    RETURN = r'\breturn\b'
    IF = r'\bif\b'
    ELSE = r'\belse\b'
    FOR = r'\bfor\b'
    NEW = r'\bnew\b'
    NULL = r'\bnull\b'

    # symbols
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    GE = r'>='
    LE = r'<='
    EQ = r'\=='
    NOTEQ = r'!='
    DIVIDE = r'/'
    GT = r'>'
    LT = r'<'
    ASSIGN = r'='
    REMAINDER = r'%'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    SEMICOL = r';'
    COL = r','

    # Identifiers
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Numbers
    INT_CONSTANT = r'[0-9]+'
    FLOAT_CONSTANT = r'[+-]?[0-9]+\.[0-9]+'

    # Strings
    STRING_CONSTANT = r'[a-zA-Z\u00C0-\u00FF]+'

    # String que contém os caracteres ignorados entre os tokens
    ignore = ' \t'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newLine(self, t):
        self.lineno = t.value.count('\n')


if __name__ == '__main__':
    data = 'x = 3 + 42 * (s - t)'
    lexer = LexerAnalyser()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
