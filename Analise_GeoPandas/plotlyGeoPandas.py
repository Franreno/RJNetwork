import plotly.express as px
import pandas as pd
import numpy as np
import json

rjPath = "./RJdata/RJ.json"
weeklyDengueDataPath = "./RJdata/Dengue_Brasil_2010-2016_Daniel.xlsx"
outputPath = "./plotlyPages/paginasGeoJSON/"

names = ['id', 'cities']
for i in range(1, 53):
    names.append(str(i))
names.append('total')

print("Abrindo dados de dengue")
weeklyDengueData = pd.read_excel(
    weeklyDengueDataPath, names=names, header=None, sheet_name=None)
weeks = np.linspace(1, 52, 52, dtype=int)
print("Aberto com sucesso")

print("Abrindo geoJSON")
with open(rjPath, "r") as geo:
    mp = json.load(geo)
print("Aberto com sucesso")

cols = ["Municipio", "Week", "Value"]
years = ["2010", "2011", "2012", "2013", "2014", "2015"]

for year in years:
    print(f"\nStatus: Ano {year}\n")

    dataDF = weeklyDengueData[year]

    print("Criando frames")
    mainDataList = []
    for i in range(len(dataDF["cities"])):
        cumulative = 0
        for week in weeks:
            cumulative += dataDF[str(week)][i]
            dataList = [dataDF["cities"][i], week, cumulative]
            mainDataList.append(dataList)
    print("Criado com sucesso")

    finalDF = pd.DataFrame(mainDataList, columns=cols)

    print("Criando figura")
    fig = px.choropleth(
        finalDF,
        locations="Municipio",
        geojson=mp,
        featureidkey="properties.NOME",
        locationmode='geojson-id',
        animation_frame="Week",
        color="Value",
        title=f"<b> Casos de Dengue por semana em {year}<b>"
    )
    print("Figura criada")

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    print("Salvando figura")
    fig.show()
    fig.write_html(outputPath + year + '.html')
    print("Sucesso...")