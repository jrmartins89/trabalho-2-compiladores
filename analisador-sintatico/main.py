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
    tokens = {DEF, INT, FLOAT, STRING, BREAK, IDENT, READ, NUMBER, LBRACE, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN,
              RPAREN, RBRACE, FLOAT_CONSTANT,INT_CONSTANT, STRING_CONSTANT, PRINT, RETURN, IF, ELSE, FOR, NEW, NULL}
    ignore = ' \t'
    literals = {'=', '+', '-', '*', '/', '(', ')', '%', 'return', '[', ']', ';'}

    # Tokens
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    FLOAT_CONSTANT = r'[-+]?[0-9]*[.][0-9]'
    INT_CONSTANT = r'[-+]?[0-9]'

    # Ignored pattern
    ignore_newline = r'\n+'

    # reserved words
    DEF     = r'def'
    INT     = r'int'
    FLOAT   = r'float'
    STRING  = r'string'
    BREAK   = r'\bbreak\b'
    READ    = r'\bread\b'
    PRINT   = r'\bprint\b'
    IF      = r'\bif\b'
    ELSE    = r'\belse\b'
    FOR     = r'\bfor\b'
    NEW     = r'\bnew\b'
    NULL = r'\bnull\b'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParser(Parser):
    debugfile = 'parser.out'
    tokens = CalcLexer.tokens

    precedence = (
        # ('left', IF, THEN), # note - if-then will be in sly-calc2.py
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', IDENT),
        ('left', STRING_CONSTANT),
    )

    def __init__(self):
        self.idents = {}
        self.prompt = True
        self.debug = False

    @_('estatement')
    def program(self, p):
        return p.estament

    @_('funclist')
    def program(self, p):
        return p.funclist

    @_('funcdef funclist1')
    def funclist(self, p):
        return p.funcdef, p.funclist1

    @_('funclist')
    def funclist1(self, p):
        return p.funclist



    @_('FLOAT')
    def expr(self, p):
        return p.FLOAT

    @_('RETURN')
    def expr(self, p):
        return p.RETURN

    @_('IDENT "=" expr')
    def statement(self, p):
        self.idents[p.IDENT] = p.expr

    @_('IDENT')
    def statement(self, p):
        self.idents[p.IDENT] = p.expr
    # note - if-then will be in sly-calc2.py
    # @_('IF expr THEN statement')
    # def statement(self, p):
    #    if p.expr:
    #        self.statement(p.statement)
    # NOTE - this will be fixed in like 15 minutes.
    # still working on it...
    # actually, needs a bit of reworking of things.  so doing that...

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 // p.expr1

    @_('expr "%" expr')
    def expr(self, p):
        return p.expr0 % p.expr1

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('NEW')
    def expr(self, p):
        return p.NEW

    @_('FLOAT_CONSTANT')
    def expr(self, p):
        return float(p.FLOAT_CONSTANT)

    @_('INT_CONSTANT')
    def expr(self, p):
        return int(p.INT_CONSTANT)

    @_('STRING_CONSTANT')
    def expr(self, p):
        return p.STRING_CONSTANT

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
