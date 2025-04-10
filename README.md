# Simulador de Autômatos Finitos Determinísticos (AFD)

Este projeto foi desenvolvido para a disciplina de **Teoria da Computação**, visando facilitar a criação, visualização, validação e minimização de Autômatos Finitos Determinísticos (AFD).

## Funcionalidades
- **Definição de AFD**: Interface amigável para definir estados, símbolos do alfabeto, estado inicial, estados finais e transições.
- **Validação de Palavras**: Verifica se uma palavra fornecida é aceita ou rejeitada pelo AFD definido.
- **Visualização do AFD**: Gera uma imagem visual do autômato usando a biblioteca Graphviz.
- **Minimização de AFD**: Reduz o AFD a uma versão mínima, simplificando sua estrutura sem alterar seu comportamento.
- **Tabela de Transições**: Exibe claramente as transições definidas no AFD.

## Tecnologias Utilizadas
- Python
- Tkinter (interface gráfica)
- Graphviz (visualização gráfica)

## Requisitos
- Python 3.x
- Graphviz instalado no sistema ([download aqui](https://graphviz.org/download/))

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Romulomdr/project_AFD.git
cd <diretorio-do-projeto>
```

2. Instale as dependências Python:
```bash
pip install graphviz
```

3. Execute o aplicativo:
```bash
python interface.py
```

## Como usar
1. Clique em "Definir AFD" para configurar o autômato.
2. Defina o alfabeto, os estados, o estado inicial, estados finais e transições.
3. Use as funcionalidades disponíveis para validar palavras, minimizar e visualizar o AFD ou exibir a tabela de transições.

## Autores
- Romulo Matheus da S. D.
- Toim Higor O. de S.