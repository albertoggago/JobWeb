#import datetime
#from pymongo import MongoClient
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import nltk as nl
#from nltk.corpus import stopwords
#from nltk.corpus import names, stopwords, words
#from nltk.corpus import names, stopwords, words, cess_esp, brown
#from stop_words import get_stop_words
#from string import punctuation
#from nltk.stem import SnowballStemmer
#from collections import defaultdict
#import math
from scipy.sparse import eye, lil_matrix, coo_matrix, vstack
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
#import smtplib
#from email.mime.text import MIMEText

#import re
#import csv
#import matplotlib as mp
#import pprint
#from matplotlib import style
#from operator import itemgetter


import sys
import datetime


#80 test 20 train
from sklearn.cross_validation import train_test_split
df_train, df_test = train_test_split(df, test_size=0.20, random_state=0)

df_train_matrix = eye(0)
df_test_matrix = eye(0)
for a in df_train.index:
    row = df_matrix.getrow(a)
    df_train_matrix = vstack([df_train_matrix, row])
for a in df_test.index:
    row = df_matrix.getrow(a)
    df_test_matrix = vstack([df_test_matrix, row])

    
    
print "# CREADAS DATAFRAMES, train: x: {0} y: {1}, test: x: {2} y: {3}".format(df_train.shape[0],                                                                               df_train.shape[1],                                                                               df_test.shape[0],                                                                               df_test.shape[1])
print "# CREADAS MATRIX, train: x: {0} y: {1}, test: x: {2} y: {3}".format(df_train_matrix.shape[0],                                                                           df_train_matrix.shape[1],                                                                           df_test_matrix.shape[0],                                                                           df_test_matrix.shape[1])


# In[4]:


def guargar_prediccion (tabla,crosstab,titulo):
    elemento = {}
    elemento["modelo"]=titulo

    if crosstab.shape[1]==3:
        elemento["tipo1"]=    100.0*crosstab.iloc[0].iloc[1]/crosstab.iloc[0].iloc[2]
        elemento["tipo2"]=    100.0*crosstab.iloc[1].iloc[0]/crosstab.iloc[1].iloc[2]
        elemento["accuracy"]= 100.0*(crosstab.iloc[1].iloc[1]+crosstab.iloc[0].iloc[0])/crosstab.iloc[2].iloc[2]
        elemento["precision"]=100.0*crosstab.iloc[1].iloc[1]/crosstab.iloc[2].iloc[1]
        elemento["recall"]=   100.0*crosstab.iloc[1].iloc[1]/crosstab.iloc[1].iloc[2]
        elemento["Fscore"]=   2.0*elemento["precision"]*elemento["recall"]/                              (elemento["precision"]+elemento["recall"])
    else:
        elemento["tipo1"]=      0.0
        elemento["tipo2"]=    100.0
        elemento["accuracy"]=   0.0
        elemento["precision"]=  0.0
        elemento["recall"]=   100.0
        elemento["Fscore"]=     0.0

    tabla.append(elemento)
    return tabla

tablaResultadosTest = []
tablaResultadosTrain = []



# In[5]:



#ejecucion del modelo naive bayess tipo Bernoulli.
clf = BernoulliNB().fit(df_train_matrix, df_train['decision'])

### PREDICCION
predicted_train_NBBernoulli = clf.predict(df_train_matrix)
ct_train = pd.crosstab(df_train['decision'], predicted_train_NBBernoulli, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_train,"Naive Bayess Bernoulli")

predicted_test_NBBernoulli = clf.predict(df_test_matrix)
ct_test = pd.crosstab(df_test['decision'], predicted_test_NBBernoulli, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_test,"Naive Bayess Bernoulli")

print "modelo Naive Bayess Bernoulli: \n{0} ".format(ct_train)
print "\n"
print "modelo Naive Bayess Bernoulli: \n{0} ".format(ct_test)


# In[6]:


#ejecucion del modelo naive bayess tipo Gaussian.
clf = GaussianNB().fit(df_train_matrix.toarray(), df_train['decision'])

### PREDICCION
predicted_train_GaussianNB = clf.predict(df_train_matrix.toarray())
ct_test = pd.crosstab(df_train['decision'], predicted_train_GaussianNB, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"Naive Bayess Gaussian")

predicted_test_GaussianNB = clf.predict(df_test_matrix.toarray())
ct_train = pd.crosstab(df_test['decision'], predicted_test_GaussianNB, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"Naive Bayess Gaussian")

print "modelo Naive Bayess Gaussian: \n{0} ".format(ct_test)
print "\n"
print "modelo Naive Bayess Gaussian: \n{0} ".format(ct_train)


# In[7]:


#ejecucion del modelo naive bayess tipo Multinomial.
clf = MultinomialNB().fit(df_train_matrix, df_train['decision'])

### PREDICCION
predicted_train_MultinomialNB = clf.predict(df_train_matrix)
ct_train = pd.crosstab(df_train['decision'], predicted_train_MultinomialNB, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"Naive Bayess Multinomial")

predicted_test_MultinomialNB = clf.predict(df_test_matrix)
ct_test = pd.crosstab(df_test['decision'], predicted_test_MultinomialNB, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"Naive Bayess Multinomial")

print "modelo Naive Bayess Multinomial: \n{0} ".format(ct_train)
print "\n"
print "modelo Naive Bayess Multinomial: \n{0} ".format(ct_test)


# In[8]:


from sklearn.linear_model import LogisticRegression

#Create linear regression object summary(linear)
model = LogisticRegression()

#Train the model using the training sets and check score
model.fit(df_train_matrix, df_train['decision'])
model.score(df_train_matrix, df_train['decision'])

predicted_train_linear = model.predict(df_train_matrix)
ct_train = pd.crosstab(df_train['decision'], predicted_train_linear, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"Logistic Regression")

predicted_test_linear = model.predict(df_test_matrix)
ct = pd.crosstab(df_test['decision'], predicted_test_linear, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"Logistic Regression")


print "modelo Logistic Regression: \n{0} ".format(ct_train)
print "\n"
print "modelo Logistic Regression: \n{0} ".format(ct_test)


# In[9]:


from sklearn.tree import DecisionTreeClassifier

#Create linear regression object summary(linear)
model = DecisionTreeClassifier(criterion='gini')

#Train the model using the training sets and check score
model.fit(df_train_matrix, df_train['decision'])
model.score(df_train_matrix, df_train['decision'])

predicted_train_linear = model.predict(df_train_matrix)
ct_train = pd.crosstab(df_train['decision'], predicted_train_linear, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"Tree")

predicted_test_linear = model.predict(df_test_matrix)
ct_test = pd.crosstab(df_test['decision'], predicted_test_linear, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"Tree")

print "modelo Tree Regression: \n{0} ".format(ct_train)
print "\n"
print "modelo Tree Regression: \n{0} ".format(ct_test)


# In[10]:


from sklearn.svm import LinearSVC

#Create linear regression object summary(linear)
model = LinearSVC()

#Train the model using the training sets and check score
model.fit(df_train_matrix, df_train['decision'])
model.score(df_train_matrix, df_train['decision'])

predicted_train_linear = model.predict(df_train_matrix)
ct_train = pd.crosstab(df_train['decision'], predicted_train_linear, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"SVM")

predicted_test_linear = model.predict(df_test_matrix)
ct_test = pd.crosstab(df_test['decision'], predicted_test_linear, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"SVM")

print "modelo SVM: \n{0} ".format(ct_train)
print "\n"
print "modelo SVM: \n{0} ".format(ct_test)


# In[11]:


from sklearn.neighbors import KNeighborsClassifier

#Create linear regression object summary(linear)
model = KNeighborsClassifier(n_neighbors=5)

#Train the model using the training sets and check score
model.fit(df_train_matrix, df_train['decision'])
model.score(df_train_matrix, df_train['decision'])

predicted_train_linear = model.predict(df_train_matrix)
ct_train = pd.crosstab(df_train['decision'], predicted_train_linear, margins=True)
tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"KNN")

predicted_train_linear = model.predict(df_test_matrix)
ct_test = pd.crosstab(df_test['decision'], predicted_test_linear, margins=True)
tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"KNN")

print "modelo KNN: \n{0} ".format(ct_train)
print "\n"
print "modelo KNN: \n{0} ".format(ct_test)


# In[12]:


from sklearn.ensemble import RandomForestClassifier


for i in range(1,200,10):
    #Create linear regression object summary(linear)
    model = RandomForestClassifier(n_estimators = i)

    #Train the model using the training sets and check score
    model.fit(df_train_matrix, df_train['decision'])

    predict = model.predict_proba(df_train_matrix)

    predicted_train_linear = model.predict(df_train_matrix)
    ct_train = pd.crosstab(df_train['decision'], predicted_train_linear, margins=True)
    tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"RForest "+str(i))

    predicted_test_linear = model.predict(df_test_matrix)
    ct_test = pd.crosstab(df_test['decision'], predicted_test_linear, margins=True)
    tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"RForest "+str(i))
    print "tipo: {0}"
    FSCORE(":", "{1}".format(i,guargar_prediccion([],ct_test,"RForest")[0]["Fscore"])")

    print "modelo Random Forest: \n{0} ".format(ct_train)
    print "\n"
    print "modelo Random Forest: \n{0} ".format(ct_test)


# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier

#Create linear regression object summary(linear)
for i in range(10,300,25):
    for j in range(1,10):
        model = GradientBoostingClassifier(n_estimators=i,learning_rate=0.1, max_depth=j, random_state=0)

        #Train the model using the training sets and check score
        model.fit(df_train_matrix.toarray(), df_train['decision'])

        predicted_train_linear = model.predict(df_train_matrix.toarray())
        ct_train = pd.crosstab(df_train['decision'], predicted_train_linear, margins=True)
        tablaResultadosTrain = guargar_prediccion(tablaResultadosTrain,ct_train,"GBM")

        predicted_test_linear = model.predict(df_test_matrix.toarray())
        ct_test = pd.crosstab(df_test['decision'], predicted_test_linear, margins=True)
        tablaResultadosTest = guargar_prediccion(tablaResultadosTest,ct_test,"GBM estimators: "+str(i)+" - "+str(j))
        print "tipo: {0} - {1}, FSCORE: {2}".format(i,j,guargar_prediccion([],ct_test,"GBM")[0]["Fscore"])

    print "modelo Gradient Boosting: \n{0} ".format(ct_train)
    print "\n"
    print "modelo Gradient Boosting: \n{0} ".format(ct_test)
    print "\n"
    print "FSCORE: {0}".format(guargar_prediccion([],ct_test,"GBM")[0]["Fscore"])


# In[ ]:


df_resultados_train = pd.DataFrame.from_dict(tablaResultadosTrain, orient='columns')

df_resultados_train.sort_values(by=["Fscore"],ascending=False)


# In[ ]:


df_resultados_test = pd.DataFrame.from_dict(tablaResultadosTest, orient='columns')

df_resultados_test.sort_values(by=["Fscore"],ascending=False)

