###
#   Celso Antonio Uliana Junior - Nov 2019
###

#   Este trabalho consiste em um chatbot para uma hamburgueria.

#   Importação de dependencias.
import os
import csv
import frases
import cardapio
import entidades
import param_grid as params

from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

#   x(texto) e y(classe)
x = []
y = []

#   Leitura de parâmetros do modulo.
p = params.regressao()

#   Cardapio e entidades e frases de resposta.
card = cardapio.dic
respostas = frases.dic
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

print('Acuracia do modelo: ', grid_search.best_score_)

classificador = LogisticRegression(random_state = grid_search.best_params_['random_state'], C = grid_search.best_params_['C'], multi_class = grid_search.best_params_['multi_class'],
solver = grid_search.best_params_['solver'], class_weight = grid_search.best_params_['class_weight'])

classificador.fit(x, y)

pedido = dict()

print('Pronto, agora é só usar!!')


while(True):
    texto = input()
    inst = vectorizer.transform([texto])
    intencao = classificador.predict(inst)

    if(intencao == 'conta'):
        print('conta')

    if(intencao == 'pedido'):
        print('pedido')

    if(intencao == 'cardapio'):
        for sessao in card:
            print('------- ', sessao, ' ----------')
            for item in card[sessao]:
                print('-> ', item, ' : R$:', card[sessao][item])

    if(intencao == 'funcionario'):
        print('funcionario')
