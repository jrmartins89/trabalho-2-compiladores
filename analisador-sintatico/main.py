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
    tokens = {DEF, INT, IGNORE, FLOAT, STRING, BREAK, IDENT, READ, NUMBER, LBRACE, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN,
              RPAREN, RBRACE, FLOAT_CONSTANT,INT_CONSTANT, STRING_CONSTANT, PRINT, RETURN, IF, ELSE, FOR, NEW, NULL}
    ignore = ' \t'
    literals = {'=', '+', '-', '*', '/', '(', ')', '%', '[', ']', ';' ','}

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
    IGNORE = r'\bignore\b'

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

    @_('INT IDENT z')
    def vardecl(self, p):
        return p.INT + p.IDENT, p.z

    @_('FLOAT IDENT z')
    def vardecl(self, p):
        return p.FLOAT + p.IDENT, p.z

    @_('STRING IDENT z')
    def vardecl(self, p):
        return p.STRING + p.IDENT, p.z

    @_('"[" INT_CONSTANT "]" z')
    def z(self, p):
        return p.INT_CONSTANT, p.z

    @_('lvalue "=" atribstat1')
    def atribstat(self, p):
        return p.lvalue, p.atribstat1

    @_('expression')
    def atribstat1(self, p):
        return p.expression

    @_('allocexpression')
    def atribstat1(self, p):
        return p.allocexpression

    @_('funccall')
    def atribstat1(self, p):
        return p.funccall

    @_('IDENT "(" paramlistcall ")" ')
    def funccall(self, p):
        return p.IDENT, p.paramlistcall

    @_('IDENT paramlistcall1')
    def paramlistcall(self, p):
        return p.IDENT, p.paramlistcall1

    @_('"," paramlistcall')
    def paramlistcall1(self, p):
        return p.paramlistcall

    @_('PRINT expression')
    def printstat(self, p):
        return p.PRINT, p.expression

    @_('READ lvalue')
    def readstat(self, p):
        return p.PRINT, p.expression

    @_('RETURN')
    def returnstat(self, p):
        return p.RETURN

    @_('IF "(" expression ")" statement s')
    def ifstat(self, p):
        return p.IF, p.expression, p.statement, p.s

    @_('ELSE statement')
    def s(self, p):
        return p.ELSE, p.statement

    @_('IGNORE')
    def s(self, p):
        return p.IGNORE

    @_('FOR "(" atribstat ";" expression ";" atribstat ")" statement')
    def forstat(self, p):
        return p.FOR, p.atribstat, p.expression, p.atribstat, p.statement

    @_('statelist statelist1')
    def statelist(self, p):
        return p.statelist, p.statelist1

    @_('statelist')
    def statelist1(self, p):
        return p.statelist

    @_('NEW t k')
    def allocexpression(self, p):
        return p.NEW, p.t, p.k

    @_('INT')
    def t(self, p):
        return p.INT

    @_('FLOAT')
    def t(self, p):
        return p.FLOAT

    @_('STRING')
    def t(self, p):
        return p.STRING

    @_(' "[" numexpression "]" k1')
    def k(self, p):
        return p.numexpression, p.k1

    @_('k')
    def k1(self, p):
        return p.k

    @_('numexpression g')
    def expression(self, p):
        return p.numexpression, p.g

    @_('p numexpression')
    def g(self, p):
        return p.p, p.numexpression

    @_('term l')
    def numexpression(self, p):
        return p.term, p.l

    @_('l1')
    def l(self, p):
        return p.l1

    @_('term unaryexpr m')
    def o(self, p):
        return p.term, p.unaryexpr, p.m

    @_('n unaryexpr')
    def m(self, p):
        return p.n, p.unaryexpr

    @_('*')
    def n(self):
        return '*'

    @_('/')
    def n(self):
        return '/'

    @_('%')
    def n(self):
        return '%'

    @_('r factor')
    def unaryexpr(self, p):
        return p.r, p.factor

    @_('+')
    def r(self):
        return '+'

    @_('-')
    def r(self):
        return '-'

    @_('INT_CONSTANT')
    def factor(self, p):
        return p.INT_CONSTANT

    @_('FLOAT_CONSTANT')
    def factor(self, p):
        return p.FLOAT_CONSTANT

    @_('STRING_CONSTANT')
    def factor(self, p):
        return p.STRING_CONSTANT

    @_('NULL')
    def factor(self):
        return 'null'

    @_('lvalue')
    def factor(self, p):
        return p.lvalue

    @_('"(" numexpression ")"')
    def factor(self, p):
        return p.numexpression

    @_('IDENT k1')
    def lvalue(self, p):
        return p.IDENT, p.k1

    @_('o term l1')
    def l1(self, p):
        return p.o, p.term, p.l1

    @_('unaryexpr "*" unaryexpr')
    def term(self, p):
        return p.unaryexpr0, p.unaryexpr1

    @_('unaryexpr "/" unaryexpr')
    def term(self, p):
        return p.unaryexpr0, p.unaryexpr1

    @_('unaryexpr "%" unaryexpr')
    def term(self, p):
        return p.unaryexpr0, p.unaryexpr1

    @_('vardecl ";"')
    def statement(self, p):
        return p.paramlist

    @_('atribstat ";"')
    def statement(self, p):
        return p.atribstat

    @_('printstat ";"')
    def statement(self, p):
        return p.printstat

    @_('readstat ";"')
    def statement(self, p):
        return p.readstat

    @_('returnstat ";"')
    def statement(self, p):
        return p.returnstat

    @_('ifstat')
    def statement(self, p):
        return p.ifstat

    @_('forstat')
    def statement(self, p):
        return p.forstat

    @_('"{" statelist "}"')
    def statement(self, p):
        return p.statelist

    @_('BREAK ";"')
    def statement(self, p):
        return p.BREAK

    @_('statement')
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

    @_('DEF IDENT "(" paramlist ")" "{" statelist "}"')
    def funcdef(self, p):
        return p.DEF, p.IDENT, p.paramlist, p.statelist

    @_('INT IDENT paramlist1')
    def paramlist(self, p):
        return p.INT, p.IDENT, p.paramlist1

    @_('FLOAT IDENT paramlist1')
    def paramlist(self, p):
        return p.FLOAT, p.IDENT, p.paramlist1

    @_('STRING IDENT paramlist1')
    def paramlist(self, p):
        return p.STRING, p.IDENT, p.paramlist1

    @_('paramlist')
    def paramlist1(self, p):
        return p.paramlist

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
