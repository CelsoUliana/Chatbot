###
#   Celso Antonio Uliana Junior - Nov 2019
###
import numpy as np

def knn():
    return  {   'metric' : ('euclidean', 'minkowski', 'manhattan' ), 
                'n_neighbors': (1,3,5,7,9,11,13,15,17,19),
                'weights' : ('uniform', 'distance')
            }

def regressao(): 
    return  {   'random_state' : [0, 42, 100],
                'C': [0.001, 1, 1000],
                'class_weight': ('balanced', None),
                'solver': ('newton-cg', 'lbfgs'),  
                'multi_class':('ovr', 'auto')
            }    

def tree():
    return  {   'criterion' : ('gini', 'entropy'), 
                'splitter' : ('best', 'random'),
                'min_samples_split' : (3, 5, 7),
                'max_depth': (1, 3, 5, 7)
            }