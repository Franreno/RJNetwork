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

cols = ["Municipio", "Ano", "Porcentagem", "Diferença", "UFRJ", "IBGE"]
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

colorValues = ['rgb(62, 171, 165)', 'rgb(0, 0, 255)', 'rgb(103, 100, 255)','rgb(203, 80, 75)','rgb(255, 165, 0)','rgb(255, 75, 0)', 'rgb(255,0,0)']

def createColorScale(data):
    ticksvals = np.linspace(0, data.max(), 7)
    x = np.linspace(0.1, 1, 7)


    colorscale = [ [0.0, 'rgb(0,255,0)' ] ]
    colorscale.append( [0.000001, 'rgb(0,255,0)'] )
    colorscale.append( [0.000001, colorValues[0]] )
    colorscale.append( [0.2, colorValues[1]] )
    colorscale.append( [0.4, colorValues[2]] )
    colorscale.append( [0.6, colorValues[3]] )
    colorscale.append( [0.8, colorValues[4]] )
    colorscale.append( [0.9, colorValues[5]] )
    colorscale.append( [1, colorValues[6]] )

    return ticksvals, colorscale


ticksvals, colorscale = createColorScale(UFRJDengueData["2010"]["total"])

colorbar = dict(
    tick0 = 0,
    tickmode = 'array',
    tickvals = ticksvals
)

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
    color="Porcentagem",
    hover_data=["Porcentagem", "Diferença", "UFRJ", "IBGE"],
    title=f"Porcentagem da diferença",
    color_continuous_scale=colorscale
)
print("Figura criada")

fig.update_geos(
    fitbounds="locations",
    visible=False
)

outputPath = "./plotlyPages/comparision/"
print("Salvando figura")
fig.show()
fig.write_html(outputPath + "Porcentagem" + '.html')
print("Sucesso...")