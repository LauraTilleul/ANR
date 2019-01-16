from stop_words import get_stop_words
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import preprocessing
from sklearn.cluster import SpectralClustering
import numpy as np
import random
import json

fp="static/original/abstracts.txt"

def getMatTermDocu(filepath=fp, threshold=0.2):

  data = pd.read_csv(filepath,sep="\t",encoding = "ISO-8859-1")
  data = data.dropna()
  data_res = data.iloc[:,1]

  stopwords = get_stop_words("french") + get_stop_words("english")
  cvec = CountVectorizer(stop_words=stopwords, min_df=1, max_df=.5)

  cvec.fit(data_res)
  cvec_counts = cvec.transform(data_res)

  transformer = TfidfTransformer()
  transformed_weights = transformer.fit_transform(cvec_counts)
  binarizer = preprocessing.Binarizer(threshold=threshold).fit(transformed_weights)

  mat_bin = binarizer.transform(transformed_weights)
  Mtd = pd.DataFrame(mat_bin.toarray(), index=data_res.index, columns= cvec.get_feature_names())

  return Mtd


def triData(Mtd):
    
  remove_zeros = Mtd.loc[:, (Mtd !=0).any(axis=0)]
  remove_zeros = remove_zeros.loc[:,remove_zeros.sum() > 1]

  delete = []
  
  for i in remove_zeros.columns :
    
    if ( '_' in i or '0' in i or '1' in i or '2' in i or '3' in i or '4' in i
         or '5' in i or '6' in i or '7' in i or '8' in i or '9' in i ):

      delete.append(i)
      
  #cols= [c for c in Mtd.columns if c not in delete]
  remove_zeros.drop(columns=delete,inplace=True)    

  return remove_zeros

def getMatrice(remove_zeros, matType):
    
  Transpose = np.transpose(remove_zeros)
  
  if matType == "terms":
      
    t = np.dot(Transpose,remove_zeros)
    cols = remove_zeros.columns

  else :
      
    t = np.dot(remove_zeros,Transpose)
    cols = remove_zeros.index
    
  mat = pd.DataFrame(t, index= cols, columns=cols)
  return mat


def selectBest(terms, nbwords,matType):
# selecing best words
  dic = {}

  for col in terms.columns:
    dic[col] = terms[col].sum()

  sorted_tuples = sorted(dic.items(),key=lambda x:x[1], reverse=True)
  
  best_vals = [i[0] for i in sorted_tuples]
  #best_sums = [i[1] for i in sorted_tuples]

  terms = terms[best_vals[:nbwords]]
  terms = terms.loc[best_vals[:nbwords],:]

  return terms

def createJson(matrice, data, matType):

  tojson={
      "nodes": [],
      "links": []
      }

  clustering = SpectralClustering(n_clusters=4, assign_labels="discretize", random_state=0, affinity='precomputed').fit(matrice.values)
  labels = clustering.labels_
  
  for i in range(len(matrice.columns)):

    if matType == "docs":

      name = data.loc[matrice.columns[i],"Acronyme"]
      indexes = np.where(matrice[matrice.columns[i]]>0)[0].tolist()

    else : 

      name = matrice.columns[i]
      indexes = np.where(matrice[name]>0)[0].tolist()

    group = labels[i]

    new={
      "group": int(group), 
      "index": i, 
      "name": name
      }
    
    if matType == "terms": 
      new["value"] = matrice[name].sum()
      
    tojson["nodes"].append(new)

    for j in indexes:
      
      if matType == "docs":
        val = matrice.loc[matrice.columns[i],matrice.columns[j]]

      else:
        val = matrice.loc[name,matrice.columns[j]]

      link={
            "source": i,
            "target": j,
            "value": val
            }

      tojson['links'].append(link)

  with open('static/dataCooc.json','w') as fp:
    json.dump(tojson, fp)


def jsonBubble(terms, remove_zeros):
    
  tojson={ 'children': [] }

  for name in terms.columns: 
    val = remove_zeros[name].sum()
    dic = {
          "Name": name,
          "Count": val
           }

    tojson["children"].append(dic)

  with open("static/dataBubble.json",'w') as fp:
    json.dump(tojson,fp)

def getDataBubble(bubbles=50):

  data = pd.read_csv(fp,sep="\t",encoding = "ISO-8859-1")
  data = data.dropna()
    
  Mtd = getMatTermDocu()
  remove_zeros = triData(Mtd)
  
  terms = getMatrice(remove_zeros,"terms")
  terms = selectBest(terms, bubbles, "terms")
  
  jsonBubble(terms,remove_zeros)

def getDataCooccurences(bubbles=50):

  data = pd.read_csv(fp,sep="\t",encoding = "ISO-8859-1")
  data = data.dropna()

  Mtd = getMatTermDocu()
  remove_zeros = triData(Mtd)
  
  terms = getMatrice(remove_zeros,"terms")
  terms = selectBest(terms, bubbles, "terms")

  createJson(terms,data,"terms")


