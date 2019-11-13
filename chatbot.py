'''
    Celso Antonio Uliana Junior - Nov 2019
'''


'''
    Este trabalho consiste em um chatbot para uma hamburgueria.
'''

'''
    Importação de dependencias.
'''
import csv
import pandas
import numpy as np
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer


x = []
y = []


'''
    Leitura de dados.
'''
with open('dataset.csv', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        y.append(row['inten'])
        x.append(row['texto'])

'''
    Transformar os dados em BOW.
'''
vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, strip_accents = 'unicode')
x = vectorizer.fit_transform(x)


'''
    Instanciar o leave one outs.
'''
loo = LeaveOneOut()
loo.get_n_splits(x)

yi = np.array(y)

y_pred = []

'''
    Usando leave one outs para treinar o KNN
'''
for train_index, test_index in loo.split(x):
    #print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = x[train_index], x[test_index]
    y_train, y_test = yi[train_index], yi[test_index]
    #print(X_train, X_test, y_train, y_test)
    model = KNeighborsClassifier(n_neighbors = 4)
    model.fit(X_train, y_train)
    val = model.predict(X_test)
    y_pred.append(val)


'''
    Metricas
'''
print('Acuracia')
print(accuracy_score(yi, y_pred))
print(accuracy_score(yi, y_pred, normalize=False))

print('precisao')
print(precision_score(yi, y_pred, average='macro'))
print(precision_score(yi, y_pred, average='micro'))
print(precision_score(yi, y_pred, average='weighted'))

print('recall score')
print(recall_score(yi, y_pred, average='macro'))
print(recall_score(yi, y_pred, average='micro'))
print(recall_score(yi, y_pred, average='weighted'))

'''
model = KNeighborsClassifier(n_neighbors = 1)
model.fit(x,yi)
'''

'''
acurracy = cross_val_score(model, x, yi, scoring = 'accuracy', cv=3)
print(acurracy)
'''

text = 'Quero um xbacon'
inst = vectorizer.transform([text])
print(model.predict(inst))