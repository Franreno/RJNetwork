import json
import numpy as np
import pandas as pd
from pandas.core.dtypes.missing import isnull
import plotly.express as px

from data import getData

rjPath = "./RJdata/RJ.json"
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


print("Abrindo geoJSON")
with open(rjPath, "r") as geo:
    mp = json.load(geo)
print("Aberto com sucesso")

cols = ["Municipio", "Ano", "Porcentagem", "Diff", "UFRJ", "IBGE"]
years = ["2010", "2011", "2012"]
IBGEDICT, UFRJDICT = getData()


mainDataList = []
#Criar o dataframe para o plotly
for i in range(len(IBGEDICT["2010"].keys())):
    for year in years:
        city = UFRJDengueData[year]["cities"][i]
        UFRJdata = float(UFRJDICT[year][city])
        IBGEdata = float(IBGEDICT[year][city])
        diff = abs(UFRJdata - IBGEdata)
        maxVal = max([UFRJdata, IBGEdata])
        if(diff != 0 and maxVal != 0 and diff != maxVal):
            percentage = (diff / maxVal) * 100
        else:
            percentage = 0
        mainDataList.append( [city, year, percentage, diff, float(UFRJdata), float(IBGEdata)] )



finalDF = pd.DataFrame(mainDataList, columns=cols)
print(finalDF)

print("Criando figura")
fig = px.choropleth(
    finalDF,
    locations="Municipio",
    geojson=mp,
    featureidkey="properties.NOME",
    locationmode='geojson-id',
    animation_frame=cols[1],
    color="Diff",
    hover_data=["Porcentagem", "Diff", "UFRJ", "IBGE"],
    title=f"Diff ano",
)
print("Figura criada")

fig.update_geos(
    fitbounds="locations",
    visible=False
)

outputPath = "./plotlyPages/comparision/"
print("Salvando figura")
fig.show()
fig.write_html(outputPath + "Diff" + '.html')
print("Sucesso...")