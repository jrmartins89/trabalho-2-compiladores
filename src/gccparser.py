from sly import Parser
from gcclexer import GCCLexer


class GCCParser(Parser):
    tokens = GCCLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', IDENT),
        ('left', STRING_CONSTANT)
    )

    @_('')
    def empty(self, p):
        pass

    @_('')
    def funclist(self, p):
        return p.empty

    @_('funcdef funclist1')
    def funclist(self, p):
        return p.funcdef, p.funclist1

    @_('funclist')
    def funclist1(self, p):
        return p.funclist

    @_('')
    def funclist1(self, p):
        return p.empty

    @_('DEF IDENT LPAREN paramlist RPAREN LBRACE statelist RBRACE')
    def funcdef(self, p):
        return p.DEF, p.IDENT, p.LPAREN, p.paramlist, p.RPAREN, p.LBRACE, p.statelist, p.RBRACE

    @_('')
    def statelist(self, p):
        return p.empty

    @_('INT IDENT paramlist1')
    def paramlist(self, p):
        return p.INT, p.IDENT, p.paramlist1

    @_('FLOAT IDENT paramlist1')
    def paramlist(self, p):
        return p.FLOAT, p.IDENT, p.paramlist1

    @_('STRING IDENT paramlist1')
    def paramlist(self, p):
        return p.STRING, p.IDENT, p.paramlist1

    @_('')
    def paramlist(self, p):
        return p.empty

    @_('COL paramlist')
    def paramlist1(self, p):
        return p.COL, p.paramlist

    @_('')
    def paramlist1(self, p):
        return p.empty

    @_('vardecl SEMICOL')
    def statement(self, p):
        return p.vardecl, p.SEMICOL

    @_('atribstat SEMICOL')
    def statement(self, p):
        return p.atribstat, p.SEMICOL

    @_('printstat SEMICOL')
    def statement(self, p):
        return p.printstat, p.SEMICOL

    @_('readstat SEMICOL')
    def statement(self, p):
        return p.readstat, p.SEMICOL

    @_('returnstat SEMICOL')
    def statement(self, p):
        return p.returnstat, p.SEMICOL

    @_('ifstat')
    def statement(self, p):
        return p.ifstat

    @_('forstat')
    def statement(self, p):
        return p.forstat

    @_('LBRACE statelist RBRACE')
    def statement(self, p):
        return p.statelist

    @_('BREAK SEMICOL')
    def statement(self, p):
        return p.BREAK, p.SEMICOL

    @_('SEMICOL')
    def statement(self, p):
        return p.SEMICOL

    @_('INT IDENT z')
    def vardecl(self, p):
        return p.INT, p.IDENT, p.z

    @_('FLOAT IDENT z')
    def vardecl(self, p):
        return p.FLOAT, p.IDENT, p.z

    @_('STRING IDENT z')
    def vardecl(self, p):
        return p.STRING, p.IDENT, p.z

    @_('LBRACKET INT_CONSTANT RBRACKET z')
    def z(self, p):
        return p.LBRACKET, p.INT_CONSTANT, p.RBRACKET, p.z

    @_('')
    def z(self, p):
        return p.empty

    @_('lvalue ASSIGN atribstat1')
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

    @_('IDENT LPAREN paramlistcall RPAREN ')
    def funccall(self, p):
        return p.IDENT, p.LPAREN, p.paramlistcall, p.RPAREN

    @_('IDENT paramlistcall1')
    def paramlistcall(self, p):
        return p.IDENT, p.paramlistcall1

    @_('')
    def paramlistcall(self, p):
        return p.empty

    @_('COL paramlistcall')
    def paramlistcall1(self, p):
        return p.COL, p.paramlistcall

    @_('')
    def paramlistcall1(self, p):
        return p.empty

    @_('PRINT expression')
    def printstat(self, p):
        return p.PRINT, p.expression

    @_('READ lvalue')
    def readstat(self, p):
        return p.PRINT, p.expression

    @_('RETURN')
    def returnstat(self, p):
        return p.RETURN

    @_('IF LPAREN expression RPAREN statement s')
    def ifstat(self, p):
        return p.IF, p.LPAREN, p.expression, p.RPAREN, p.statement, p.s

    @_('ELSE statement')
    def s(self, p):
        return p.ELSE, p.statement

    @_('FOR LPAREN atribstat SEMICOL expression SEMICOL atribstat RPAREN statement')
    def forstat(self, p):
        return p.FOR, p.LPAREN, p.atribstat, p.SEMICOL, p.expression, p.SEMICOL, p.atribstat, p.RPAREN, p.statement

    @_('statelist statelist1')
    def statelist(self, p):
        return p.statelist, p.statelist1

    @_('statelist')
    def statelist1(self, p):
        return p.statelist

    @_('')
    def statelist1(self, p):
        return p.empty

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

    @_('LBRACKET numexpression RBRACKET k1')
    def k(self, p):
        return p.LBRACKET, p.numexpression, p.RBRACKET, p.k1

    @_('k')
    def k1(self, p):
        return p.k

    @_('')
    def k1(self, p):
        return p.empty

    @_('numexpression g')
    def expression(self, p):
        return p.numexpression, p.g

    @_('p numexpression')
    def g(self, p):
        return p.p, p.numexpression

    @_('')
    def g(self, p):
        return p.empty

    @_('LT')
    def p(self, p):
        return p.LT

    @_('GT')
    def p(self, p):
        return p.GT

    @_('LE')
    def p(self, p):
        return p.LE

    @_('GE')
    def p(self, p):
        return p.GE

    @_('EQ')
    def p(self, p):
        return p.EQ

    @_('NOTEQ')
    def p(self, p):
        return p.NOTEQ

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

    @_('')
    def m(self, p):
        return p.empty

    @_('TIMES')
    def n(self, p):
        return p.TIMES

    @_('DIVIDE')
    def n(self, p):
        return p.DIVIDE

    @_('REMAINDER')
    def n(self, p):
        return p.REMAINDER

    @_('n unaryexpr')
    def unaryexpr1(self, p):
        return p.n, p.unaryexpr

    @_('unaryexpr unaryexpr1')
    def term(self, p):
        return p.unaryexpr, p.unaryexpr1

    @_('r factor')
    def unaryexpr(self, p):
        return p.r, p.factor

    @_('PLUS')
    def r(self, p):
        return p.PLUS

    @_('MINUS')
    def r(self, p):
        return p.MINUS

    @_('')
    def r(self, p):
        return p.empty

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

    @_('LPAREN numexpression RPAREN')
    def factor(self, p):
        return p.LPAREN, p.numexpression, p.RPAREN

    @_('IDENT k1')
    def lvalue(self, p):
        return p.IDENT, p.k1

    @_('o term l1')
    def l1(self, p):
        return p.o, p.term, p.l1

    @_('')
    def l1(self, p):
        return p.empty
