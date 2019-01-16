import pandas as pd
from scripts_python import script_gender

data=pd.read_csv("data_anr.csv",sep=";")

coord=script_gender.getSexeCoordinateurs()
data["Sexe"]=coord["Sexe"]

new=pd.DataFrame()
#new=data[["Durée en mois", "Montant","Sexe"]]

new["duree"]=data["Durée en mois"]
new["montant"]=data["Montant"]
new["sexe"]=data["Sexe"]

new=new.dropna()

new.to_csv("scatter_plot.csv", index=False)
