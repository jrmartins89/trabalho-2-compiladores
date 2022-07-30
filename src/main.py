import sys
from gcclexer import GCCLexer
from sly import lex
from gccparser import GCCParser

if __name__ == '__main__':
    lexer = GCCLexer()
    text = True
    while True:
        try:
            if len(sys.argv) <= 1:
                print('\n\n################Analisador Lexico########################\n')
                text = input('Insira o caminho do arquivo: '
                             ' ../../trabalho-2-compiladores/codigosLCC/codigo1.lcc \n'
                             'Para acessar os outros arquivos basta trocar o nome do arquivo para os nomes '
                             '"codigo2.lcc" ou "codigo3.lcc" no final do caminho do arquivo. Digite "sair" para sair do programa\n\n'
                             'caminho ->')
                if text == 'sair':
                    text = False
                    break
            lexText = open(text, 'r').read()
            print(lexText)
        except EOFError:
            break
        try:
            if lexText:
                lexResult = lexer.tokenize(lexText)
                for token in lexResult:
                    print(token)
        except lex.LexError as e:
            print(e)

    print('\n\n\n\n')

    while text:
        print('################Analisador Sintático########################\n\n')
        parser = GCCParser()
        try:
            result = parser.parse(lexer.tokenize(lexText))
            print(result)
        except EOFError:
            break
