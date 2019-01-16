import pandas as pd


def getDataBasicStats():

    data = pd.read_csv("static/original/data_anr.csv", sep=';')
    
    newdata = pd.DataFrame()
    years = [year for year in range(min(data["Année de financement"]),max(data["Année de financement"])+1)]
    newdata["Année"] = years

    budgetTotal = [] # pas de montants en 2016
    nbProjets = []
    budgetsMoyen = [] # pas de montants en 2016
    dureeMoyenne = [] # pas renseigné en 2009 et 2016.
    
    for year in years:

        dataYear = data[data["Année de financement"] == year]

        budgetTot = dataYear["Montant"].sum()
        budgetTotal.append(budgetTot)

        nbProj = len(dataYear)
        nbProjets.append(nbProj)

        moyenne = dataYear["Montant"].mean()
        budgetsMoyen.append(moyenne)

        dureeMoy = dataYear["Durée en mois"].mean()
        dureeMoyenne.append(dureeMoy)
    

    newdata["Budget Total"] = budgetTotal
    newdata["Nombre de Projets"] = nbProjets
    newdata["Budget Moyen par Projet"] = budgetsMoyen
    newdata["Durée en mois Moyenne des Projets"] = dureeMoyenne

    newdata.to_csv("static/basicStats.tsv",sep="\t", index=False) #fillna(0)
