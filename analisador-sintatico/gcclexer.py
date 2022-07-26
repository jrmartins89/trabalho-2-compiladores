from sly import Lexer


class GCCLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {DEF, IDENT, NUMBER, PLUS, MINUS, TIMES,
              DIVIDE, ASSIGN, LPAREN, RPAREN, LBRACE,
              RBRACE, LBRACKET, RBRACKET, INT, FLOAT, STRING,
              SEMICOL, BREAK, COL, READ, PRINT, RETURN, IF, ELSE, FOR, NEW,
              GT, LT, GE, LE, EQ, NOTEQ, REMAINDER, INT_CONSTANT, FLOAT_CONSTANT, STRING_CONSTANT, NULL}

    # String containing ignored characters between tokens
    ignore = ' \t'

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
    FLOAT_CONSTANT = r'[0-9]+(.[0-9]*)?'

    # Strings
    STRING_CONSTANT = r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')'''

    @_(r'\d+')
    def INT_CONSTANT(self, t):
        t.value = int(t.value)
        return t

    @_(r'[0-9]+(.[0-9]*)?')
    def FLOAT_CONSTANT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\"[a-zA-Z\u00C0-\u00FF]+\"')
    def STRING_CONSTANT(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newLine(self, t):
        self.lineno = t.value.count('\n')

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text
