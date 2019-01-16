import pandas as pd
import json

def getDataPartners():

    data = pd.read_csv("static/original/data_anr.csv", sep=';')
    partenaires = data["Libellé de partenaire"].dropna().values.tolist()

    listpart = []

    for p in partenaires:
        for ps in p.split(';'):
            listpart.append(ps)

    setpartners = list(set(listpart))
    count = []

    for p in setpartners:
        count.append(listpart.count(p))

    new = pd.DataFrame()
    new["Partenaire"] = setpartners
    new["count"] = count

    new = new.sort_values(by="count")

    bestPartners = new.loc[new.index[-31:],:]

    bestPartners = bestPartners.reset_index()

    nodes = []

    for i in bestPartners.index:

        nodes.append( {
                        "id": i,
                        "name": bestPartners.loc[i,"Partenaire"] 
                       })

    df = pd.DataFrame( columns=bestPartners["Partenaire"].values.tolist(), index=bestPartners["Partenaire"].values.tolist())
    df = df.fillna(0)

    for p in partenaires:
        lis = p.split(';')

        for i in range(len(lis)):
            for j in range(i+1,len(lis)):

                if (lis[i] in df.index and lis[j] in df.index):
                    df.loc[lis[i],lis[j]]+=1     
    
    links = []

    df = (df-df.min())/(df.max()-df.min())

    for partner in df.index:
        for partner2 in df.index:

            id1 = bestPartners[bestPartners["Partenaire"] == partner ].index[0].item()
            id2 = bestPartners[bestPartners["Partenaire"] == partner2].index[0].item()
            
            links.append( {
                            "source": id1,
                            "target": id2,
                            "weight": df.loc[partner,partner2].item()
                           })
    
    dic = { "nodes": nodes, "edges": links }

    with open("static/dataPartners.json","w") as fp:
        json.dump(dic,fp)

    return df


