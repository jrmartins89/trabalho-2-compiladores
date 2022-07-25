from sly import Lexer, Parser
import sys

slyPath = "/u1/h0/jkinne/public_html/cs420-s2019/code/sly-0.4"
sys.path.append(slyPath)


class CalcLexer(Lexer):
    # Set of token names. This is always required
    tokens = {NUMBER, STRING_CONSTANT, INT_CONSTANT, FLOAT_CONSTANT, IDENT, IF, ELSE, PRINT, PLUS, MINUS, TIMES,
              DIVIDE, ASSIGN, EQ, LT, LE, GT, GE, NE, RETURN, FOR, NEW, DEF,
              READ, IGNORE, BREAK, NULL, STRING, INT, FLOAT, REMAINDER}
    literals = {'(', ')', '{', '}', ';', '[', ']', '%'}
    # String containing ignored characters
    ignore = ' \t'
    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQ = r'=='
    ASSIGN = r'='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    INT_CONSTANT = r'[0-9]+'
    FLOAT_CONSTANT = r'(^[+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?$)'
    REMAINDER = r'%'

    @_(r'\d+')
    def number(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['if'] = IF
    IDENT['else'] = ELSE
    IDENT['print'] = PRINT
    IDENT['read'] = READ
    IDENT['return'] = RETURN
    IDENT['ignore'] = IGNORE
    IDENT['new'] = NEW
    IDENT['for'] = FOR
    IDENT['null'] = NULL
    IDENT['break'] = BREAK
    IDENT['string'] = STRING
    IDENT['float'] = FLOAT
    IDENT['int'] = INT

    STRING_CONSTANT = r'[a-zA-Z\u00C0-\u00FF]+'
    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
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
        return p.INT, p.IDENT, p.z

    @_('FLOAT IDENT z')
    def vardecl(self, p):
        return p.FLOAT, p.IDENT, p.z

    @_('STRING IDENT z')
    def vardecl(self, p):
        return p.STRING, p.IDENT, p.z

    @_('"[" INT_CONSTANT "]" z')
    def z(self, p):
        return p.INT_CONSTANT, p.z

    @_('term l')
    def numexpression(self, p):
        return p.term, p.l

    @_('numexpression g')
    def expression(self, p):
        return p.numexpression, p.g

    @_('expression')
    def atribstat1(self, p):
        return p.expression

    @_('lvalue EQ atribstat1')
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

    @_('p numexpression')
    def g(self, p):
        return p.p, p.numexpression

    @_('l1')
    def l(self, p):
        return p.l1

    @_('term unaryexpr m')
    def o(self, p):
        return p.term, p.unaryexpr, p.m

    @_('n unaryexpr')
    def m(self, p):
        return p.n, p.unaryexpr

    @_('PLUS')
    def n(self, p):
        return p.PLUS

    @_('DIVIDE')
    def n(self, p):
        return p.DIVIDE

    @_('REMAINDER')
    def n(self, p):
        return p.REMAINDER

    @_('r factor')
    def unaryexpr(self, p):
        return p.r, p.factor

    @_('PLUS')
    def r(self, p):
        return p.PLUS

    @_('MINUS')
    def r(self, p):
        return p.MINUS

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
        return p.NULL

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

    @_('n unaryexpr')
    def unaryexpr1(self, p):
        return p.n, p.unaryexpr

    @_('unaryexpr unaryexpr1')
    def term(self, p):
        return p.unaryexpr, p.unaryexpr1

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

    @_('paramlist')
    def paramlist1(self, p):
        return p.paramlist

    @_('INT IDENT paramlist1')
    def paramlist(self, p):
        return p.INT, p.IDENT, p.paramlist1

    @_('vardecl ";"')
    def statement(self, p):
        return p.paramlist

    @_('FLOAT IDENT paramlist1')
    def paramlist(self, p):
        return p.FLOAT, p.IDENT, p.paramlist1

    @_('DEF IDENT "(" paramlist ")" "{" statelist "}"')
    def funcdef(self, p):
        return p.DEF, p.IDENT, p.paramlist, p.statelist

    @_('STRING IDENT paramlist1')
    def paramlist(self, p):
        return p.STRING, p.IDENT, p.paramlist1

    @_('IDENT "=" expr')
    def statement(self, p):
        self.idents[p.IDENT] = p.expr

    @_('IDENT')
    def statement(self, p):
        self.idents[p.IDENT] = p.expr

    @_('LT')
    def p(self, p):
        return p.LT

    @_('GT')
    def p(self, p):
        return p.GT

    @_('EQ')
    def p(self, p):
        return p.EQ

    @_('LE')
    def p(self, p):
        return p.LE

    @_('GE')
    def p(self, p):
        return p.GE

    @_('NE')
    def p(self, p):
        return p.NE

    @_('PLUS')
    def p(self, p):
        return p.PLUS

    @_('DIVIDE')
    def p(self, p):
        return p.DIVIDE

    @_('MINUS')
    def p(self, p):
        return p.MINUS

    @_('ASSIGN')
    def p(self, p):
        return p.ASSIGN

    @_('TIMES')
    def p(self, p):
        return p.TIMES
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
        return int(p.number)

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


if __name__ == '__main__':
    data = ''
    lexer = CalcLexer()

    for tok in lexer.tokenize(data):
        print(tok)

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
