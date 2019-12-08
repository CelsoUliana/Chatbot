###
#   Celso Antonio Uliana Junior - Nov 2019
###

#   Este trabalho consiste em um chatbot para uma hamburgueria.

#   Importação de dependencias.
import os
import csv
import frases
import random
import funcoes
import cardapio
import entidades
import datetime as dt
import param_grid as params

from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer


#   x(texto), y(classe), flag para a conversa e hora do dia atual.
x = []
y = []
flag = 1
pedido = {}
hora = dt.datetime.today().hour

#   Leitura de parâmetros do modulo.
p = params.regressao()

#   Cardapio e entidades e frases de resposta.
card = cardapio.dic
respostas = frases.dic
mapeador = entidades.enum
etiquetador = entidades.dic

#   Leitura do dataset.
with open('dataset.csv', newline = '', encoding = 'utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        y.append(row['inten'])
        x.append(row['texto'])

#   Transformar os dados em BOW(bag of words).
vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, strip_accents = 'unicode')
x = vectorizer.fit_transform(x)

#   Instanciar o leave one outs.
loo = LeaveOneOut()
loo.get_n_splits(x)

print('Aguarde, o bot está sendo treinado...')

grid_search = GridSearchCV(LogisticRegression(), p, scoring = 'accuracy', cv = loo, iid = False)
grid_search.fit(x, y)

print('Acuracia do modelo =~ ', grid_search.best_score_)

classificador = LogisticRegression(random_state = grid_search.best_params_['random_state'], C = grid_search.best_params_['C'], multi_class = grid_search.best_params_['multi_class'],
solver = grid_search.best_params_['solver'], class_weight = grid_search.best_params_['class_weight'])

classificador.fit(x, y)

print('Pronto, agora é só usar!!')

while(True):

    if flag:
        #   bom dia
        if hora > 6 and hora < 12:
            print(random.choice(respostas['cumprimento']['manha']))

        #   boa tarde
        if hora > 12 and hora < 18:
            print(random.choice(respostas['cumprimento']['tarde']))
        #   boa noite
        if hora > 18:
            print(random.choice(respostas['cumprimento']['noite']))

    flag = 0

    texto = input()
    inst = vectorizer.transform([texto])
    intencao = classificador.predict(inst)

    if intencao == 'conta':
        
        valor = 0

        if pedido is not None:
            for chave in pedido:
                valor = valor + cardapio.mapeador[chave] * pedido[chave]

        if valor == 0:
            print('Voce ainda não pediu nada!')
        
        else:

            print(random.choice(respostas['conta']), valor)

            if hora > 6 and hora < 12:
                print(random.choice(respostas['despedida']['manha']))

            if hora > 12 and hora < 18:
                print(random.choice(respostas['despedida']['tarde']))

            if hora > 18 or hora >= 0 and hora < 6:
                print(random.choice(respostas['despedida']['noite']))

            #   Limpeza de variaveis relacionadas ao uso, simulando o termino de uma conversa.
            flag = 1
            pedido = {}

    if intencao == 'pedido':
        pedido_local = funcoes.reconhece_entidades(etiquetador, texto)
        if((pedido_local is not None) and ('num' in pedido_local) and ('pedidos' in pedido_local)):
            funcoes.mapeia_itens(pedido_local, mapeador, pedido)
            print(random.choice(respostas['pedido']))
        else:
            print(random.choice(respostas['erro']))


    if intencao == 'cardapio':
        print(random.choice(respostas['cardapio']))
        for sessao in card:
            print('------- ', sessao, ' ----------')
            for item in card[sessao]:
                print('\t', item, ' \tR$:', card[sessao][item])

    if intencao == 'funcionario':
       print(random.choice(respostas['funcionario']))