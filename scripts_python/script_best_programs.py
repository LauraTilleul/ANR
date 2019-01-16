import pandas as pd
import json
from scripts_python import script_gender


def getDataPrograms(sex="all"):

    data = pd.read_csv("static/original/data_anr.csv",sep=';')

    coords = script_gender.getSexCoordinateurs()
    data["Sexe"] = coords["Sexe"]

    tojson={}
    
    if sex == "femme":
        data = data[data["Sexe"] == "F"]

    if sex == "homme":
        data = data[data["Sexe"] == "M"]

    years=list(set(data["Année de financement"]))

    for year in years:

        select = data[data["Année de financement"] == year]
        programs = list(set(select["Programme"]))
        
        count=[]

        for prog in programs:
            count.append(len(select[select["Programme"] == prog] ))

        new=pd.DataFrame()

        new["Programme"] = programs
        new["counts"] = count

        bests = new.sort_values( by="counts" )
        bests = bests.loc[new.index[-10:],:]
       
        array=[]

        for i in bests.index:
            
            dic = { 
                    "name" : bests.loc[i,"Programme"],
                    "values": int(bests.loc[i,"counts"])
                  }
                
            array.append(dic)

        tojson[year] = array

    with open("static/programsByGender"+sex.capitalize()+".json", "w") as fp:
                     json.dump(tojson,fp)
        
    
