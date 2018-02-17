
# coding: utf-8

# # Proceso de analisis Diario de todos los correos
# 
# ## carga de datos y librerias

# In[1]:


import datetime
from datetime import timedelta
from pymongo import MongoClient
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import nltk as nl
from nltk.corpus import stopwords
#from nltk.corpus import names, stopwords, words
#from nltk.corpus import names, stopwords, words, cess_esp, brown
from stop_words import get_stop_words
from string import punctuation
from nltk.stem import SnowballStemmer
from collections import defaultdict
import math
from scipy.sparse import lil_matrix, coo_matrix, vstack
from sklearn.naive_bayes import GaussianNB
import smtplib
from email.mime.text import MIMEText
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import json

#variables generales
#determina cuantas repeticiones tiene que tener un palabra para que se mantenga
#colchon = 10
#colchon = 1000
colchon = 50

print "## INFO ## INICIO: {0}".format(datetime.datetime.now())


# ## conexion a la base de datos Mongo

# In[ ]:


#client = MongoClient('localhost:27017', ssl=True, ssl_ca_certs='/home/alberto/datos/ssl/mongodb.pem', ssl_match_hostname=False) 
#client.the_database.authenticate("posiciones","posicionesX",source="admin")
url =  'mongodb://posiciones:1984ZuloPase@'
url += 'cluster0-shard-00-00-wapx6.mongodb.net:27017,'
url += 'cluster0-shard-00-01-wapx6.mongodb.net:27017,'
url += 'cluster0-shard-00-02-wapx6.mongodb.net:27017/'
url += 'posiciones?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client = MongoClient(url)

db = client["posiciones"]
param = db.correoUrl.find_one()
if param == None:
    print "base de datos parada o param no inicializado"
else:
    print "-- INFO -- Conexion a base de datos OK"

print "# BASE DE DATOS CONECTADA "


# ## cargamos los datos 

# In[ ]:


df = pd.DataFrame.from_records(db.correoUrl.find())
#quitamos los nules que haya en titulo y summary
dfmod = df[df[["titulo","summary"]].isnull().apply(lambda x: not np.any(x),axis=1)]
dfmod = dfmod.fillna("")

print "# CARGAMOS DATOS, filas: {0}, columnas: {1}".format(dfmod.shape[0],dfmod.shape[1])


# ## creamos la linea de texto

# In[ ]:


dfmod["texto"] = dfmod["titulo"].str.cat([" "] * dfmod.shape[0])                                     .str.cat(dfmod["company"])                                                           .str.cat([" "] * dfmod.shape[0]).str.cat(dfmod["donde"])                             .str.cat([" "] * dfmod.shape[0]).str.cat(dfmod["observaciones"])                     .str.cat([" "] * dfmod.shape[0]).str.cat(dfmod["summary"])

print "# CREADA COLUMNA TEXTO"

tokenizacion = []
for fila in dfmod.index:
    tokenizacion.append([word.lower() for word in nl.wordpunct_tokenize(dfmod['texto'][fila])])

dfmod["token"] = tokenizacion

print "# TOKENIZACION, filas: {0}, columnas: {1}".format(dfmod.shape[0],dfmod.shape[1])


# ## Cargamos diccionarios de stopwords en distintos idiomas. Añadimos catalán. 

# In[ ]:


# me voy a generar un diccionario de palabras por cada uno de los lenguajes del corpus del nltk 
stopwords_set = {}

for language in stopwords.fileids():
#   lenguaje kazajo no lo encentro en las stop_words, así que no lo tengo en cuenta
    if language != u'kazakh':
        stopwords_set[language] = set(get_stop_words(language))
        
# me voy a generar una lista de lenguajes que tenemos 
lenguajes = stopwords.fileids()
del lenguajes[lenguajes.index(u'kazakh')]

print "# IDIOMAS CARGADOS: {0}".format(len(lenguajes))


# ## Calculo de los ratios de los lenguajes
# 
# ### funcion _calculate_languages_ratios --- buscamos el ratio de las palabras para determinar el lenguaje 
# ### funcion detect_language --- calculamos el lenguaje del texto

# In[ ]:


def _calculate_languages_ratios(words):

    languages_ratios = {}
    words_set = set(words)
    
# Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in lenguajes:
        common_elements = words_set.intersection(stopwords_set[language])
        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios

#----------------------------------------------------------------------
def detect_language(words):

    ratios = _calculate_languages_ratios(words)

    #most_rated_language = max(ratios, key=ratios.get)
    ratios_sorted = sorted(ratios.items(),key=lambda x: x[1], reverse = True)
    
    #si el primero no es ingles o español lo cambiamos por el segundo
    if ratios_sorted[0][0] in ['spanish','english']:
        if ratios_sorted[0][0] == 'english' and            ratios_sorted[1][0] == 'spanish' and            ratios_sorted[0][1] == (ratios_sorted[1][1]+1) :
            print ("XXXXXXXXXXXXXXXXXXXXX")
            print ("idioma: "+ratios_sorted[0][0]+" ratio: "+str(ratios_sorted[0][1])+" cambiado por ")
            print ("idioma: "+ratios_sorted[1][0]+" ratio: "+str(ratios_sorted[1][1]))
            print ("XXXXXXXXXXXXXXXXXXXXX")
            return ratios_sorted[1][0]
    else:
          if ratios_sorted[1][0] in ['spanish','english']:
            print ("XXXXXXXXXXXXXXXXXXXXX")
            print ("idioma: "+ratios_sorted[0][0]+" ratio: "+str(ratios_sorted[0][1])+" cambiado por ")
            print ("idioma: "+ratios_sorted[1][0]+" ratio: "+str(ratios_sorted[1][1]))
            print ("XXXXXXXXXXXXXXXXXXXXX")
            return ratios_sorted[1][0]

    return ratios_sorted[0][0]

# Asignación de idioma y prueba de la misma

dfpa = dfmod
if 'lenguaje' in dfmod.columns:
    del dfmod["lenguaje"]
lenguaje = {}

for fila in dfpa.index:
    lenguaje[fila] = detect_language(dfpa['token'][fila])

# inserto una nueva columna en el data frame con el idioma en el que se encuentra la descripcion a tratar
dfpa["lenguaje"] =  lenguaje.values()

dfmod = dfpa

dfpa.groupby(list(['lenguaje'])).size()

print "# LENGUAJES EN LAS TABLAS: \n{0}".format(dfpa.groupby(list(['lenguaje'])).size())


# ## Eliminamos stopwords, signos de puntuacion y números
# 
# ### funcion _eliminar_palabras quita las palabras stop words del idioma que hemos asignado

# In[ ]:


# eliminar palabras de una lista dada
#-------------------------------------------------
def _eliminar_palabras(words, lista):

    corpus = [word for word in words if word not in lista]
    return corpus

# ELIMINACIÓN DE STOPWORDS
corpus_clave = {}
for fila in dfmod.index:
    corpus_clave[fila] = _eliminar_palabras(dfmod['token'][fila], list(stopwords_set[dfmod['lenguaje'][fila]]))

# inserto una nueva columna en el data frame con el corpus del texto, eliminando las stopwords
dfmod["corpus"] = corpus_clave.values()

#for a in dfmod[dfmod['lenguaje']=="english"]:
#    print(dfmod['corpus'][30:])

print "# ELIMINAR STOPWORDS: columnas: {0}".format(dfmod.shape[1])


# ## ELIMINACIÓN DE SIGNOS DE PUNTUACION

# In[ ]:


#añadimos signos de puntuacion nuevos:
lista_puntuacion = list(punctuation)
lista_nueva =["++","++,",".,",").","):","),",":(",".(",".","->","·","->","…)","...)","..)",".)","”,"]
lista_nueva =[]
for ele in lista_nueva:
    lista_puntuacion.append(ele)
corpus_clave = {}

for fila in dfmod.index:
    corpus_clave[fila] = _eliminar_palabras(dfmod['corpus'][fila], lista_puntuacion)

# inserto una nueva columna en el data frame con el corpus del texto, eliminando las stopwords
dfmod["corpusA"] = corpus_clave.values()

print "# QUITAMOS SIGNOS DE PUNTUACION: columnas: {}".format(dfmod.shape[1])


# ## quitar numeros
# 
# ### funcion no_es_numero --- determina cuando algo es numero o no si lo es lo quitamos el diccionario

# In[ ]:


# determinar por funcion si una palabra es un numero
#---------------------------------------------------
def no_es_numero(n):
    try:
        float(n)
    except ValueError:
        return True
    return False


# ELIMINACIÓN DE NUMEROS
corpus_clave = {}

for fila in dfmod.index:
    corpus_clave[fila] = [word for word in dfmod['corpusA'][fila] if no_es_numero(word)]

# inserto una nueva columna en el data frame con el corpus del texto, eliminando las stopwords
dfmod["corpusB"] = corpus_clave.values()

#no proceso errores ortográficos
dfmod["corpusC"] = dfmod["corpusB"]

print "# QUITAMOS NUMEROS: columnas: {0}".format(dfmod.shape[1])


# ## lematizacion

# In[ ]:


# LEMATIZACION 
dict_stemmer = {}
for lenguaje in SnowballStemmer.languages:
    dict_stemmer[lenguaje] = SnowballStemmer(lenguaje)


#realizamos la lematizacion
lematizacion = []
for fila in dfmod.index:
    lematizacion.append([dict_stemmer[dfmod["lenguaje"][fila]].stem(t) for t in dfmod["corpusC"][fila]])

# inserto una nueva columna en el data frame con la lematizacion (raices de las palabras) de la descripcion a tratar
#pruebo sin lematizacion me da los mismos resultados no lo uso.
#dfmod["lema"] = lematizacion
dfmod["lema"] = dfmod["corpusC"]

print "# GENERACION LEMATIZACION: columnas: {0}".format(dfmod.shape[1])


# ## limpiamos las palabras menos usadas
# 
# #### Con las palabras que se repiten muy poco las quitamos ya que no son relevantes para el modelo
# 
# 

# In[ ]:


# ### analizar moldelos usamos bayes
# uso este ejemplo.
# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# 
# La idea es con los lemas realizar dos matrices de repeticion y procesar un modelo bayes con los train (decision == "NO" o "SI") y sacar el resutado con los test (decision == "").
# 
# Para empezar saco los tokens simples de los lemas mas bigramas y trigramas.


# In[23]:
# elimino las palabras que aparecen menos de 10 veces, ya que no me aportan nada

#creamos un conjunto mas manejable con solo los datos a procesar
dfmodMinimo = dfmod[list(['_id','decision','lema','fecha'])]
dfmodMinimo = dfmodMinimo.reset_index()

vocabulary = {}
for fila in dfmodMinimo.index:
    tokens = dfmodMinimo['lema'][fila]

    bi_tokens = nl.bigrams(tokens)
    tri_tokens = nl.trigrams(tokens)
    tokens = [token for token in tokens if len(token) > 2]
    bi_tokens = ['_'.join(token) for token in bi_tokens]
    tri_tokens = ['_'.join(token) for token in tri_tokens]

    final_tokens = []
    final_tokens.extend(tokens)
    final_tokens.extend(bi_tokens)
    final_tokens.extend(tri_tokens)

    vocabulary[fila] = (final_tokens)

lista_tokens = list(vocabulary.values())

#calculo la frecuencia
frequency = defaultdict(int)
suma = 0
for lista in lista_tokens:
    for token in lista:
        frequency[token] += 1
        suma +=1

suma      
#sumamos los elementos de de lista

lista_tokens_reducido = [[token for token in lista if frequency[token] > colchon] for lista in lista_tokens]

print "# TOKENS REDUCIDO: filas: {0}".format(len(lista_tokens_reducido))


# In[ ]:


## despues de reducir la frecuencia vamos a sacar la frecuencia de cada elemento

# In[24]:

def freq(word, doc):
    return doc.count(word)

def word_count(doc):
    return len(doc)

def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))

docs = {}
fila = 0

for final_tokens in lista_tokens_reducido:

    docs[fila] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': [], }

    for token in final_tokens:
        #The frequency computed for each fila
        docs[fila]['freq'][token] = freq(token, final_tokens)
        #The term-frequency (Normalized Frequency)
        docs[fila]['tf'][token] = tf(token, final_tokens)
        docs[fila]['tokens'] = final_tokens

    fila += 1

# Generar Inverse-Document-Frequency (IDF) y después el TF-IDF
def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
            float(frequency[word]))

def tf_idf(word, doc, idf_calculado):
    return (tf(word, doc) * idf_calculado)

for doc in docs:
    for token in docs[doc]['tf']:
        #The Inverse-Document-Frequency
        docs[doc]['idf'][token] = idf(token, lista_tokens_reducido)
        #The tf-idf
        docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], docs[doc]['idf'][token])

# tokens ordenados

words = {}

for doc in docs:
#    if doc < muestra:
        for token in docs[doc]['tf-idf']:
            if token not in words:
                words[token] = docs[doc]['tf-idf'][token]
            else:
                if docs[doc]['tf-idf'][token] > words[token]:
                    words[token] = docs[doc]['tf-idf'][token]

print "# TOKENS ORDENADOS: tokens: {0}".format(len(words))


# ## DIVIDIMOS LAS PALABRAS EN TEST Y TRAIN

# In[ ]:


# words son todas las palabras.
# Voy a construir una matrix con las repeticiones

tf_idf_lista = {}
for i in range(dfmodMinimo.shape[0]):
    tf_idf_lista[i] = docs[i]['tf-idf']
dfmodMinimo['tf-idf'] = tf_idf_lista.values()   


df_train = dfmodMinimo[dfmodMinimo['decision']!='']
df_train = df_train.reset_index()

df_test = dfmodMinimo[dfmodMinimo['decision']=='']
df_test = df_test.reset_index()

print "# DIVIDIDO TRAIN Y TEST,train: {0}, test: {1}".format(df_train.shape[0],df_test.shape[0])


# ## DUPLICAMOS LOS DATOS DEL ULTIMO MES PARA QUE TENGAN MAS PESO

# In[ ]:


#ts_mes = datetime.combine(datetime.time(),timedelta(days=-30))
timeLimit = pd.datetime.now()- pd.Timedelta(days=30)
df_add = df_train[pd.to_datetime(df_train['fecha']) > timeLimit]

print "# DATOS DEL MES,train: {0}, test: {1}".format(df_add.shape[0],df_add.shape[0])


# ## creamos las matrices para el modelo

# In[ ]:


words_columns = words.keys()

df_train_matrix = lil_matrix((df_train.shape[0],len(words_columns)))

for i in df_train.index:
    for clave, valor in df_train['tf-idf'][i].items():
        if valor >0:
            df_train_matrix[i, words_columns.index(clave) ]  = valor

df_test_matrix = lil_matrix((df_test.shape[0],len(words_columns)))

for i in df_test.index:
    for clave, valor in df_test['tf-idf'][i].items():
        if valor > 0:
            df_test_matrix[i, words_columns.index(clave) ]  = valor

print "# CREADAS MATRICES,train: x: {0} y: {1}, test: x: {2} y: {3}".format(df_train_matrix.get_shape()[0],                                                                             df_train_matrix.get_shape()[1],                                                                             df_test_matrix.get_shape()[0],                                                                              df_test_matrix.get_shape()[1])


# In[ ]:


#duplico tanto la informacion en df_tran como en df_train_matrix
df_train_add = df_train
df_train_matrix_add = df_train_matrix
for a in df_add.index:
    df_train_add = df_train_add.append(df_train.loc[a,:],ignore_index=True)
    row = df_train_matrix_add.getrow(a)
    df_train_matrix_add = vstack([df_train_matrix_add, row])
    
df_train = df_train_add
df_train_matrix = df_train_matrix_add

print "# Añadimos datos ultimo mes,train: x: {0} y: {1}, test: x: {2} y: {3}"                                       .format(df_train_matrix.get_shape()[0],                                               df_train_matrix.get_shape()[1],                                               df_test_matrix.get_shape()[0],                                                df_test_matrix.get_shape()[1])


# ## Guardo la informacion para despues usarse

# In[ ]:


def save_sparse_matrix(filename, x):
    x_coo = x.tocoo()
    row = x_coo.row
    col = x_coo.col
    data = x_coo.data
    shape = x_coo.shape
    np.savez(filename, row=row, col=col, data=data, shape=shape)

def load_sparse_matrix(filename):
    y = np.load(filename)
    z = sparse.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])
    return z

path = "/home/alberto/datos/modelosCorreos/"
save_sparse_matrix(path+"df_train_matrix",df_train_matrix)
save_sparse_matrix(path+"df_test_matrix",df_test_matrix)
df_train.to_csv(path+"df_train.df")
df_test.to_csv(path+"df_test.df")

print "Guardamos las Matrices y dataframe para su uso posterior"


# ## Procesamos los 3 mejores Modelos
# ### MODELO GAUSSIAN NAIVES BAYES
# ### MODELO RANDOM FOREST 61 arboles
# ### MODELO GBM  110 arboles y 6 de produndidad

# In[ ]:


Models = [{"Model":"Gaussian Naives Bayes"},           {"Model":"Random Forest","estimators":61},           {"Model":"GBM","estimators":110,"max_depth":6}]
df_train['modelos'] = df_train["_id"].apply (lambda x: json.JSONEncoder().encode([]))
df_test['modelos'] = df_test["_id"].apply (lambda x: json.JSONEncoder().encode([]))
df_train["porcentPREDAvg"] = 0
df_test["porcentPREDAvg"] = 0
crosstab = []


def cargar (x,modelo,decision,porcent):
    ele = json.JSONDecoder().decode(x)
    ele.append({"modelo": modelo,"decisionPRED":decision, "porcentPRED" :porcent}) 
    return json.JSONEncoder().encode(ele)


for model in Models:
    modelo = model["Model"]
    if modelo == "Gaussian Naives Bayes":
        clf = GaussianNB()
        model_clf = clf.fit(df_train_matrix.toarray(), df_train['decision'])
    elif modelo == "Random Forest":
        estimators = model["estimators"]
        clf = RandomForestClassifier(n_estimators = estimators)
        model_clf = clf.fit(df_train_matrix, df_train['decision'])
    elif modelo == "GBM":
        estimators = model["estimators"]
        max_depth = model["max_depth"]
        clf = GradientBoostingClassifier(n_estimators=estimators,learning_rate=0.1,                                          max_depth=max_depth, random_state=0)
        model_clf = clf.fit(df_train_matrix, df_train['decision'])
    else:
        break
    
    # PARTE TRAIN
    predicted_train = model_clf.predict(df_train_matrix.toarray())
    if modelo in  ["Gaussian Naives Bayes","GBM"]:
        predicted_train_proba = model_clf.predict_log_proba(df_train_matrix.toarray())
    else:
        predicted_train_proba = model_clf.predict_proba(df_train_matrix)

    # calcumanos la prediccion
    maximo = predicted_train_proba.min() *(1.0)
    minimo = predicted_train_proba.max() *(1.0)

    predicted_train_probaOK = []
    for cat,ele in zip(predicted_train,predicted_train_proba):
        if cat == 'SI':
            valor = (ele[0]-minimo) / (maximo-minimo)*100.0
        else:
            valor = (ele[1]-minimo) / (maximo-minimo)*100.0
        predicted_train_probaOK.append(valor)   

    df_train['modelo']   = modelo
    df_train["decisionPRED"] = predicted_train
    df_train["porcentPRED"]  = predicted_train_probaOK
    df_train['modelos'] = df_train.apply(lambda x:cargar(x["modelos"],x["modelo"],x["decisionPRED"],x["porcentPRED"]),axis=1)
    df_train["porcentPREDAvg"] = df_train["porcentPREDAvg"] +(df_train["decisionPRED"]=="SI") * df_train["porcentPRED"]                                    - df_train["porcentPRED"] / 2.0 + 50.0

    

    cantidadSI = 0
    cantidadNO = 0
    #parte TEST

    if df_test.shape[0]>0:
        predicted_test = model_clf.predict(df_test_matrix.toarray())
        if modelo in  ["Gaussian Naives Bayes","GBM"]:
            predicted_test_proba = model_clf.predict_log_proba(df_test_matrix.toarray())
        else:
            predicted_test_proba = model_clf.predict_proba(df_test_matrix)

        maximo = predicted_test_proba.min() *(1.0)
        minimo = predicted_test_proba.max() *(1.0)
        predicted_test_probaOK = []

        for cat,ele in zip(predicted_test,predicted_test_proba):
            if cat == 'SI':
                valor = (ele[0]-minimo) / (maximo-minimo)*100.0
            else:
                valor = (ele[1]-minimo) / (maximo-minimo)*100.0
            predicted_test_probaOK.append(valor)   

        df_test['modelo']   = modelo
        df_test["decisionPRED"] = predicted_test
        df_test["porcentPRED"]  = predicted_test_probaOK
        df_test['modelos'] = df_test.apply(lambda x:cargar(x["modelos"],x["modelo"],x["decisionPRED"],x["porcentPRED"]),axis=1)
        df_test["porcentPREDAvg"] = df_test["porcentPREDAvg"] +(df_test["decisionPRED"]=="SI") * df_test["porcentPRED"]                                     - df_test["porcentPRED"] / 2.0 + 50.0
    
        #print df_test['modelos'].head()
        cantidadSI = df_test[df_test["decisionPRED"]=="SI"].shape[0]
        cantidadNO = df_test[df_test["decisionPRED"]=="NO"].shape[0]

        print "# PROCESADO TRAIN Y TEST, modelo {0}".format(model["Model"])
    else:
        print "# NO HAY DATOS TEST, modelo {0}".format(model["Model"])
        
    ct = pd.crosstab(df_train['decision'], predicted_train, margins=True)
    crosstab.append({"modelo":modelo,"ct":ct,"cantidadSI":cantidadSI,"cantidadNO":cantidadNO})
  
df_train["porcentPREDAvg"] = df_train["porcentPREDAvg"] / len(Models)
df_test["porcentPREDAvg"] = df_test["porcentPREDAvg"] / len(Models)


#print len(Models)
#print df_train.head()
#print df_test.head()
    


# In[ ]:


# In[21]:

### cargamos los datoas en la tabla
def act_DB(temp_id,modelos, temp_tf_idf, porcentPREDAvg ):
    corpus = []
    for palabraX, frecuencia  in temp_tf_idf.items():
        corpus.append({"palabra":palabraX,"frecuencia":frecuencia})
        mod = json.JSONDecoder().decode(modelos)
    return db.correoUrl.update_one({"_id":temp_id},                                                               
                                   {"$set":{"modelos":mod, \
                                            "corpus": corpus, \
                                           "porcentPREDAvg":porcentPREDAvg },                        \
                                            "$unset":{"decisionPRED":"","decisionPRED_RF":"","porcentPRED":"","porcentPRED_RF":""}}).modified_count
    
resultadoTRAIN = df_train.apply(lambda x: act_DB(x["_id"],x["modelos"], x["tf-idf"], x["porcentPREDAvg"]), axis=1)
print "# PROCESADO TRAIN, filas: {0}".format(sum(resultadoTRAIN))

#parte TEST
if df_test.shape[0]>0:
    resultadoTEST = df_test.apply(lambda x: act_DB(x["_id"],x["modelos"], x["tf-idf"], x["porcentPREDAvg"]), axis=1)
    print "# PROCESADO TEST, filas: {0}".format(sum(resultadoTEST))
else:
    print "no hay datos TEST"


# ## parte de CROSTAB y ESTADISTICAS
# 
# ### datos_prediccion se usa para sacar toda la informacion de un crostab

# In[ ]:


def datos_prediccion (crosstab):
    elemento = {}
    
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

    return elemento


print "## INFO ## Inicio: {0}".format(datetime.datetime.now())


# ## envio del correo

# In[ ]:


#envio de correo

smtp_ssl_host = 'mail.albertoggago.es'
smtp_ssl_port = 465
username = 'albertoggagocurro@albertoggago.es'
password = 'Gemaxana1973#'
sender = username
targets = ['albertoggago@gmail.com']
msgTxt = ""
#añadimos los modelos
for ct_ampliado in crosstab:
    ct = ct_ampliado["ct"]
    prediccion = datos_prediccion(ct)
    msgTxt = msgTxt + ct_ampliado["modelo"]
    msgTxt = msgTxt + "\n "+ ""
    msgTxt = msgTxt + "\n "+ ct.to_string()
    msgTxt = msgTxt + "\n "+ ""
    msgTxt = msgTxt + "\n "+ "Type I  - Error:     "+str(prediccion["tipo1"])
    msgTxt = msgTxt + "\n "+ "Type II - Error:     "+str(prediccion["tipo2"])
    msgTxt = msgTxt + "\n "+ "Exactitud accurancy: "+str(prediccion["accuracy"])
    msgTxt = msgTxt + "\n "+ "Precision precision: "+str(prediccion["precision"])
    msgTxt = msgTxt + "\n "+ "Recall:              "+str(prediccion["recall"])
    msgTxt = msgTxt + "\n "+ "F1 Score:            "+str(prediccion["Fscore"])
    msgTxt = msgTxt + "\n "+ ""
    msgTxt = msgTxt + "\n "+ ""
    if (ct_ampliado["cantidadSI"] >0) or (ct_ampliado["cantidadNO"] >0):
        msgTxt = msgTxt + "\n "+ "filas SI: "+str(ct_ampliado["cantidadSI"])
        msgTxt = msgTxt + "\n "+ "filas NO: "+str(ct_ampliado["cantidadNO"])
        msgTxt = msgTxt + "\n "+ "filas :   "+str(ct_ampliado["cantidadSI"]+ct_ampliado["cantidadNO"])
        msgTxt = msgTxt + "\n "+ ""
        msgTxt = msgTxt + "\n "+ ""

msg = MIMEText(msgTxt)
print(msgTxt)

msg['Subject'] = 'Estadisticas Proceso'
msg['From'] = sender
msg['To'] = ', '.join(targets)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
#server.set_debuglevel(2)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()

print "## INFO ## FIN: {0}".format(datetime.datetime.now())

