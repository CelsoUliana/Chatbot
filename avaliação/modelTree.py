###
#   Celso Antonio Uliana Junior - Nov 2019
###

#   Este trabalho consiste em um chatbot para uma hamburgueria.

#   Importação de dependencias.
import csv
import pandas
import numpy as np
import param_grid as params

from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer

#   x(texto) e y(classe).
x = []
y = []

#   Leitura de parâmetros do modulo.
p = params.tree()

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

#   Instanciar um np array e y predito.
yi = np.array(y)
y_pred = []

#   Usando leave one outs para treinar a árvore.
for train_index, test_index in loo.split(x):
    X_train, X_test = x[train_index], x[test_index]
    y_train, y_test = yi[train_index], yi[test_index]

    #   Fine-tuning dos parâmetros.
    #   p é o param grid, cv = 5 é o novo default de cross validation interno e iid = False pois warning.
    grid_search = GridSearchCV(DecisionTreeClassifier(), p, scoring = 'accuracy', cv = 5, iid = False)
    grid_search.fit(X_train, y_train)

    #   Modelo Arvore de decisão.
    model = DecisionTreeClassifier(criterion = grid_search.best_params_['criterion'], splitter = grid_search.best_params_['splitter'],
    min_samples_split = grid_search.best_params_['min_samples_split'], max_depth = grid_search.best_params_['max_depth'])

    #   Fit no modelo com x_train e y_train e adicionando o valor
    #   predito numa lista de y_pred.
    model.fit(X_train, y_train)
    val = model.predict(X_test)
    y_pred.append(val)

#   Metricas do modelo Tree que estão no txt.
print('\nAcuracia')
print(accuracy_score(yi, y_pred))
print(accuracy_score(yi, y_pred, normalize = False))

print('\nprecisao')
print(precision_score(yi, y_pred, average = 'macro'))
print(precision_score(yi, y_pred, average = 'micro'))
print(precision_score(yi, y_pred, average = 'weighted'))

print('\nrecall score')
print(recall_score(yi, y_pred, average = 'macro'))
print(recall_score(yi, y_pred, average = 'micro'))
print(recall_score(yi, y_pred, average = 'weighted'))