# Analisadores léxico e sintático da linguagem LCC-2021-2
Repositório para armazenamento do código relacionado ao trabalho 2 da disciplina INE5622-06238 - Introdução a Compiladores 

Realizado por:
Arthur Machado Capaverde (17207215),
José Ribamar Marçal Martins Junior (15101188),
Luiz Andre Ventura Gosling (16203896),
Matheus Miranda Torres Gomes (18100867)
Pedro Henrique Azevedo (14201116)

## Estrutura do código

Os analisadores foram desenvolvidos na linguagem python, com framework utilizado sendo SLY, e permite o desenvolvimento dos analisadores léxico e sintático. A especificação da linguagem está dentro do proprio código do analisador sintático.

A estrutura do projeto se dá da seguinte maneira:
src/
    gcclexer.py    
    gccparser.py
    main.py
    parser.out
Makefile
requirements.txt
codigosLCC/
    codigo1.lcc
    codigo2.lcc
    codigo3.lcc

Onde:
- Os arquivos `gcclexer.py` e `gccparser.py` são o analisador léxico e sintático, respectivamente;
- O arquivo `requirements.txt` se refere aos pacotes a serem instalados para execução do código;
- Os arquivos dentro da pasta `codigosLCC/` serão os codigos a serem executados dentro de `gcclexer.py` e `gccparser.py`
- O arquivo `src/main.py` orquestrará a execução do sistema
- O arquivo `Makefile` servirá para instalação dos requisitos e preparação do sistema para compilação/interpretação/execução;
- O resultado da execução do parser será armazenado no caminho `src/parser.out`.
- O arquivo `ChomskyNormalForm.txt` apresenta a linguagem normalizada.


## Para compilar    

1. Basta rodar `make setup` e serão executados os passos necessários para preparação do ambiente

Existe o comando `make clean` para limpar a pasta target.

## Para rodar
 
O próprio `make setup` diz o que fazer, mas segue: 

Para Executar basta rodar: 

`python src/main.py caminho/relatico/para/seu/arquivo.lcc`

Exemplo de caminho relativo: `"./codigosLCC/codigo1.lcc"`

## Arquivos exemplos
Como requisitado no enunciado do trabalho, existem 3 arquvios de codigo LCC-2021-2
com extensão .lcc; 

Os mesmos estão localizados na pasta `codigosLCC`.