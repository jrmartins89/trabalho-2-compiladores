import sys
from gcclexer import GCCLexer
from sly import lex
from gccparser import GCCParser

if __name__ == '__main__':
    lexer = GCCLexer()
    while True:
        try:
            if len(sys.argv) <= 1:
                print('################Analisador Lexico########################\n')
                text = input('Insira o caminho do arquivo: '
                             ' ../../trabalho-2-compiladores/codigosLCC/codigo1.lcc \n'
                             'Para acessar os outros arquivos basta trocar o nome do arquivo para os nomes '
                             '"codigo2.lcc" ou "codigo3.lcc" no final do caminho do arquivo.\n\n'
                             'caminho ->')
            lexText = open(text, 'r').read()
            print(lexText)
        except EOFError:
            break
        try:
            if lexText:
                lexResult = lexer.tokenize(lexText)
                for token in lexResult:
                    print(token)
                break
        except lex.LexError as e:
            print(e)

    print('\n\n\n\n')

    print('################Analisador Sintático########################\n\n')
    parser = GCCParser()
    while True:
        try:
            result = parser.parse(lexer.tokenize(lexText))
            print(result)
        except EOFError:
            break
