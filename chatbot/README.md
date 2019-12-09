# Trabalho de IA 2019 - 2
Trabalho de IA, fazer um chatbot.

Celso Antonio Uliana Junior 2014.1907.003-7

Andamento do trabalho pode ser acompanhado pelo link:

https://github.com/CelsoUliana/Chatbot

Melhor modelo entre os 3 foi o de regressão logistica.
de acordo com o comparativo no comparação.txt (que uso os prints de cada um dos chatbot(modelos))

Para executar, extraia os conteudos da pasta chatbot em uma pasta local.

Tendo em vista que o dataset foi levemente alterado depois da primeira entrega(alguns campos removidos).

Depois:
    $ cd chatbot

Instalar dependecias: 
    $ pip install sklearn

Depois, rode com:
    $ python chatbot.py

## Notas sobre o trabalho
Problemas encontrados: Integração com o Telegram(É possível receber e classificar, porém, acontece um comportamento estranho na hora de enviar mensagens)
 
Palavras que estão uma dentro da outra, como por exemplo água e água com gás, do jeito que o etiquetador de entidades funciona
água com gás irá ser mapeada dentro de água também.
 
Para adicionar novos itens ao cardápio, requer um trabalho manual grande, entidades do usuário (xburger) para entidades reais(x-burger)
que estão presente no cardápio.
Possivelmente seria melhor utilizar um banco de dados(?) e/ou um regex.
