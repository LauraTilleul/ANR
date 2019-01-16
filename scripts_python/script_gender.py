import pandas as pd
import numpy as np
import gender_guesser.detector as gender
import json

d = gender.Detector()
data = pd.read_csv("static/original/data_anr.csv",sep=";")

# sexe des coordinateurs 
def getSexCoordinateurs():

    coordinateurs = data['Coordinateur du projet']
    coordinateurs = coordinateurs.to_frame()#.dropna()
    
    for i in coordinateurs.index:
        
        sex = ''
        res1 = coordinateurs.loc[i,"Coordinateur du projet"]
        
        if res1 != res1 :
            sex="U"
            
        else :

            res = res1.split(" ")
            first = res[0].capitalize()
            
            if ( res[0].isupper() == True and res[1].isupper() == False and len(res[1])>1):
                first = res[1].capitalize()

            if ( list(first)[0] == '(' ):
                sex = "U"
            
            elif ( first == "Madame"):
                sex = "F"
            
            elif ( first == "Monsieur"):
                sex = "M"

            else :
                
                first = first.split("-")[0]
                sex = getSexPerson(first)
                
                if sex == "U" :
                    sex = tryCorrections(first)

        coordinateurs.loc[i,"Sexe"] = sex
    
    return coordinateurs


def getSexPerson(name):
    
    guess = d.get_gender(name)
    
    if ( guess == "female" or guess == "mostly_female" ):
        sex = "F"
    
    elif ( guess== "male" or guess == "mostly_male"):
        sex = "M"
    
    else :
        sex = "U"

    return sex

def tryCorrections(name):
    
        namesCorrections = [ name.replace('c','ç') , name.replace("i","î"), name.replace("e","é",1), name.replace("e","è",1), name.replace("e","ê",1)]

        for names in namesCorrections :

            sex = getSexPerson(names)

            if sex != "U" :
                return sex

        return "U"


def formatDataToJson():

    coord=getSexCoordinateurs()

    data["Sexe"]=coord["Sexe"]
    array=[]

    years=list(set(data["Année de financement"]))
    years.sort()
    
    for year in years:
        
        dataYear = data[data["Année de financement"] == year]

        countFemme = len(dataYear[dataYear["Sexe"] == "F"])
        countHomme = len(dataYear[dataYear["Sexe"] == "M"])
        countInc = len(dataYear[dataYear["Sexe"] == "U"])
                     
        dico= { "year":str(year),
                "femme": countFemme,
                "homme": countHomme,
                "inconnu": countInc 
              }

        array.append(dico)
                     
    dic={ "genders": array }

    with open("static/dataGender.json","w") as fp:
        json.dump(dic,fp)

    return dic





    
