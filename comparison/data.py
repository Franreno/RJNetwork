import numpy as np
import pandas as pd

def getData():
    rjPath = "./RJdata/RJ.json"
    ibgePath = "./RJdata/dengueIBGE.csv"
    ufrjPath = "./RJdata/Dengue_Brasil_2010-2016_Daniel.xlsx"

    names = ['id', 'cities']
    for i in range(1, 53):
        names.append(str(i))
    names.append('total')

    print("Abrindo dados de dengue")
    UFRJDengueData = pd.read_excel(
        ufrjPath, names=names, header=None, sheet_name=None)
    weeks = np.linspace(1, 52, 52, dtype=int)
    print("Aberto com sucesso")


    print("Abrindo dados IBGE")
    IBGEDengueData = pd.read_csv(ibgePath)
    print("Aberto com sucesso")

    cols = ["Municipio", "Ano", "Porcentagem", "Diff", "UFRJ", "IBGE"]
    years = ["2010", "2011", "2012"]

    mainDataList = []
    IBGEDICT = {}
    UFRJDICT = {}

    for year in years:
        IBGEDICT[year] = {}
        isNull = pd.isna(IBGEDengueData[year])
        for i in range(len(IBGEDengueData["Localidade"])):
            data = IBGEDengueData[year][i]
            if(data != '-' and isNull[i] == False ):
                IBGEDICT[year][IBGEDengueData["Localidade"][i]] = int(data)
            else:
                IBGEDICT[year][IBGEDengueData["Localidade"][i]] = 0
            

        UFRJDICT[year] = {}
        for i in range(len(UFRJDengueData[year]["cities"])):
            UFRJDICT[year][UFRJDengueData[year]["cities"][i]] = int(UFRJDengueData[year]["total"][i])
            
    return IBGEDICT, UFRJDICT
