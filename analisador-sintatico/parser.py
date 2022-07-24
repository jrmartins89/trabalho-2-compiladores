from sly import Parser
from lexeranalyser import LexerAnalyser


class ParserAnalyser(Parser):
    # Carregar a lista de tokens do analisador lexico
    tokens = LexerAnalyser.tokens

    #Regras gramaticais e açoes
    @_('STATEMENT')
    def program(self, p):
        return p.statement

    @_('FUNCLIST')
    def program(self, p):
        return p.funclist

    @_('FUNCDEF FUNCLIST')
    def funclist(self, p):
        return p.funcdef + p.funclist

    @_('FUNCDEF')
    def funclist(self, p):
        return p.funcdef

    @_('def ident lparen PARAMLIST rparen lbrace STATELIST rbrace')
    def funcdef(self, p):
        return p.DEF + p.IDENT + p.LPAREN, self.paramlist, p.RPAREN + p.LBRACE, self.statelist, p.RBRACE

    @_('int ident', 'PARAMLIST')
    def paramlist(self, p):
        return p.paramlist

    @_('float ident', 'PARAMLIST')
    def paramlist(self, p):
        return p.paramlist

    @_('string ident', 'PARAMLIST')
    def paramlist(self, p):
        return p.paramlist

    @_('int ident')
    def paramlist(self, p):
        return p.INT + p.IDENT

    @_('float ident')
    def paramlist(self, p):
        return p.FLOAT + p.IDENT

    @_('string ident')
    def paramlist(self, p):
        return p.STRING + p.IDENT

    @_('STATEMENT')
    def statelist(self, p):
        return p.statement

    @_('STATEMENT STATELIST')
    def statelist(self, p):
        return p.statement, p.statelist

    @_('vardecl semicolon')
    def statement(self, p):
        return p.vardecl

    @_('atribstat semicolon')
    def statement(self, p):
        return p.atribstat

    @_('printstat semicolon')
    def statement(self, p):
        return p.PRINT

    @_('readstat semicolon')
    def statement(self, p):
        return p.READ

    @_('returnstat semicolon')
    def statement(self, p):
        return p.RETURN

    @_('ifstat')
    def statement(self, p):
        return p.IF

    @_('forstat')
    def statement(self, p):
        return p.FOR

    @_('lbrace STATELIST rbrace')
    def statement(self, p):
        return p.statelist

    @_('break semicolon')
    def statement(self, p):
        return p.BREAK

    @_('semicolon')
    def statement(self, p):
        return p.SEMICOL

    @_('int ident Z')
    def vardecl(self, p):
        return p.INT + p.IDENT, p.Z

    @_('float ident Z')
    def vardecl(self, p):
        return p.FLOAT + p.IDENT, p.Z

    @_('string ident Z')
    def vardecl(self, p):
        return p.STRING + p.IDENT, p.Z

    @_('lbrace STATELIST rbrace Z')
    def z(self, p):
        return p.statelist, p.z

    @_('TERM L')
    def numexpression(self, p):
        return p.term, p.l

    @_('NUMEXPRESSION G')
    def expression(self, p):
        return p.numexpression, p.g

    @_('lvalue eq EXPRESSION')
    def atribstat(self, p):
        p.value = p.expression
        return p.value

    @_('lvalue eq ALLOCEXPRESSION')
    def atribstat(self, p):
        p.value = p.allocexpression
        return p.value

    @_(' ident comma  PARAMLISTCALL')
    def paramlistcall(self, p):
        return p.IDENT + p.COMMA, p.paramlistcall

    @_('ident')
    def paramlistcall(self, p):
        return p.IDENT

    @_('print EXPRESSION')
    def printstat(self, p):
        return p.PRINT, p.expression

    @_('read lvalue')
    def readstat(self, p):
        return p.READ + p.LVALUE

    @_('return')
    def returnstat(self, p):
        return p.RETURN

    @_('if lparen EXPRESSION rparen STATEMENT S')
    def ifstat(self, p):
        return p.IF + p.LPAREN, p.expression, p.RPAREN, p.statement, p.s

    @_('else STATEMENT')
    def s(self, p):
        return p.ELSE, p.statement

    @_('lvalue eq FUNCCALL')
    def atribstat(self, p):
        p.value = p.funccall
        return p.value

    @_('ident lparen PARAMLISTCALL rparen')
    def funccall(self, p):
        return p.IDENT + p.LPAREN, p.paramlistcall, p.RPAREN

    @_('for lparen ATRIBSTAT semicolon EXPRESSION semicolon ATRIBSTAT rparen STATEMENT')
    def forstat(self, p):
        return p.FOR + p.LPAREN, p.atribstat + p.SEMICOLON, p.atribstat + p.RPAREN, p.statement

    @_('new T K  lbracket NUMEXPRESSION rbracket')
    def allocexpression(self, p):
        return p.NEW, p.t, p.k, p.LBRACKET, p.numexpression,p.RBRACKET

    @_('int')
    def t(self, p):
        return p.INT

    @_('float')
    def t(self, p):
        return p.FLOAT

    @_('string')
    def t(self, p):
        return p.STRING

    @_('lbracket NUMEXPRESSION rbracket K')
    def k(self,p):
        return p.LBRACKET, p.numexpression, p.RBRACKET, p.k

    @_('P  NUMEXPRESSION')
    def g(self, p):
        return p.p, p.numexpression

    @_('<')
    def p(self,p):
        return p.LT

    @_('>')
    def p(self, p):
        return p.GT

    @_('<=')
    def p(self, p):
        return p.LE

    @_('>=')
    def p(self, p):
        return p.GE

    @_('==')
    def p(self, p):
        return p.EQ

    @_('!=')
    def p(self, p):
        return p.NOTEQ

    @_(' L O TERM')
    def l(self, p):
        return p.l, p.o, p.term

    @_('+')
    def o(self, p):
        return p.PLUS

    @_('-')
    def o(self, p):
        return p.MINUS

    @_('UNARYEXPR M')
    def term(self, p):
        return p.unaryexpr, p.m

    @_('N   UNARYEXPR')
    def m(self, p):
        return p.n,p.unaryexpr

    @_('*')
    def n(self, p):
        return p.TIMES

    @_('/')
    def n(self, p):
        return p.DIVIDE

    @_('R FACTOR')
    def unaryexpr(self, p):
        return p.r, p.factor

    @_('+')
    def r(self, p):
        return p.PLUS

    @_('-')
    def r(self, p):
        return p.MINUS

    @_('int_constant')
    def factor(self, p):
        return p.INT_CONST

    @_('float_constant')
    def factor(self, p):
        return p.FLOAT_CONST

    @_('string_constant')
    def factor(self, p):
        return p.STRING_CONST

    @_('null')
    def factor(self,p):
        return p.NULL

    @_('LVALUE')
    def factor(self, p):
        return p.lvalue

    @_('lparen NUMEXPRESSION rparen')
    def factor(self, p):
        return p.LPAREN, p.numexpression, p.LPAREN

    @_('ident K')
    def lvalue(self, p):
        return p.IDENT, p.k


if __name__ == '__main__':
    lexer = LexerAnalyser()
    parser = ParserAnalyser()
    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
