# note - use python3
# note - example from https://github.com/dabeaz/sly
# note - type ctrl-d as the end of input.

# notes on lexer
# - tokens are compiled with re.verbose flag
#   (comments with #, gets rid of white space).
#   If you need to match # use \#
# - tokens matched in order in your file.
#   If you want to use == and =, put the rule for == first.
# - sometimes there is more than one way to do something in the
#   lexer.  for example, can have a separate rule for each keyword
#   or catch them under a generic "ID" or "NAME" rule and use "token remapping"

# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

# package isn't installed at the moment, so add the path so python can find it
import sys

slyPath = "/u1/h0/jkinne/public_html/cs420-s2019/code/sly-0.4"
sys.path.append(slyPath)

from sly import Lexer, Parser


class CalcLexer(Lexer):
    tokens = {IDENT, NUMBER, LBRACE, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, MOD, RBRACE, FLOAT_CONSTANT}
    ignore = ' \t'
    # Tokens
    MOD = r'%'
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    FLOAT_CONSTANT = r'[-+]?[0-9]*[.][0-9]'

    # NAME['if'] = IF # note - if-then will be in sly-calc2.py
    # NAME['then'] = THEN

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        # ('left', IF, THEN), # note - if-then will be in sly-calc2.py
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MOD),
        ('right', UMINUS),
    )

    def __init__(self):
        self.idents = {}
        self.prompt = True
        self.debug = False

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('IDENT ASSIGN expr')
    def statement(self, p):
        self.idents [p.IDENT] = p.expr

    # note - if-then will be in sly-calc2.py
    # @_('IF expr THEN statement')
    # def statement(self, p):
    #    if p.expr:
    #        self.statement(p.statement)
    # NOTE - this will be fixed in like 15 minutes.
    # still working on it...
    # actually, needs a bit of reworking of things.  so doing that...

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('expr MOD expr')
    def expr(self, p):
        return p.expr0 % p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('LBRACE expr RBRACE')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('FLOAT_CONSTANT')
    def expr(self, p):
        return float(p.FLOAT_CONSTANT)

    @_('IDENT')
    def expr(self, p):
        try:
            return self.idents[p.IDENT]
        except LookupError:
            print(f'Undefined ident {p.IDENT!r}')
            return 0


def evaluate(tree):
    global idents

    rule = tree[0]
    if rule == 'statement-expr':
        value = evaluate(tree[1])
        print(value)
        return value
    elif rule == 'assign':
        value = evaluate(tree[2])
        ident = tree[1]
        idents[ident] = value
        return value
    elif rule == 'times':
        return evaluate(tree[1]) * evaluate(tree[2])
    elif rule == 'plus':
        return evaluate(tree[1]) + evaluate(tree[2])
    elif rule == 'minus':
        return evaluate(tree[1]) - evaluate(tree[2])
    elif rule == 'divide':
        return evaluate(tree[1]) / evaluate(tree[2])
    elif rule == 'uminus':
        return -evaluate(tree[1])
    elif rule == 'number':
        return int(tree[1])
    elif rule == 'ident':
        return idents[tree[1]]
    elif rule == 'paren':
        return evaluate(tree[1])
    elif rule == 'if-then':
        value = evaluate(tree[1])
        if value:
            return evaluate(tree[2])
        else:
            return 0
    elif rule == 'while':
        while evaluate(tree[1]):
            evaluate(tree[2])


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            if parser.prompt:
                text = input('calc > ')
            else:
                text = input('')
        except EOFError:
            break
        if text:
            if parser.debug:
                print("text is - " + text)
                x = list(lexer.tokenize(text))
                print(x)
                x = iter(x)
                parser.parse(x)
            else:
                parser.parse(lexer.tokenize(text))
