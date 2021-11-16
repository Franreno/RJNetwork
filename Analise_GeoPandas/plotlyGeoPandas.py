import plotly.express as px
import pandas as pd
import numpy as np
import json

rjPath = "./RJdata/RJ.json"
weeklyDengueDataPath = "./RJdata/Dengue_Brasil_2010-2016_Daniel.xlsx"
dadosMunicipaisPath = "./RJdata/dadosMunicipiosRJ.xlsx"


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


dadosMunicipais = pd.read_excel(dadosMunicipaisPath)
dadosMunicipais = dadosMunicipais.rename(columns={'População_estimada_pessoas': 'Pop'})

def createWeeklyData(dataDF):
    mainDataList = []
    for i in range(len(dataDF["cities"])):
        cumulative = 0
        for week in weeks:
            cumulative += dataDF[str(week)][i]
            dataList = [dataDF["cities"][i], week, cumulative]
            mainDataList.append(dataList)
    return mainDataList

def createMediaMovelSimples(dataDF):
    mainDataList = []
    for i in range(len(dataDF["cities"])):
        j=0
        month=0
        while(j < 52):
            cumulative = 0
            
            while(j % 4 != 0 or j == 0):
                cumulative += dataDF[str(weeks[j])][i]
                j+=1
            
            cumulative /= 4
            dataList = [dataDF["cities"][i], month, cumulative]
            mainDataList.append(dataList)
            month+=1
            j+=1
        
    cols[1] = "Month"

    return mainDataList


def createMediaMovelPonderada(dataDF, outputPath, titleStr):
    pass

for year in years:
    print(f"\nStatus: Ano {year}\n")

    dataDF = weeklyDengueData[year].join(dadosMunicipais["Pop"])

    typeIndex = 2

    titleStr = [f"Casos de Dengue por semana em {year}",
                f"Casos de Dengue por semana com população em {year}" 
                f"Casos de Dengue média móvel em {year}",
                f"Casos de Dengue média móvel com população em {year}"]

    outputPath = [
        "./plotlyPages/paginasGeoJSON/byWeeks/",
        "./plotlyPages/paginasGeoJSON/byWeeksWithPopulation/",
        "./plotlyPages/paginasGeoJSON/bySimpleMovingAverage/",
        "./plotlyPages/paginasGeoJSON/bySimpleMovingAverageWithPopulation/"
    ]

    functions = [
        createWeeklyData(dataDF),
        createWeeklyData(dataDF),
        # createWeeklyDataWithPopulation(dataDF),
        createMediaMovelSimples(dataDF), 
        # createMediaMovelSimplesWithPopulation(dataDF), 
    ]

    print("Criando frames")
    # mainDataList = createWeeklyData(dataDF)
    mainDataList = functions[typeIndex]
    print("Criado com sucesso")
    

    finalDF = pd.DataFrame(mainDataList, columns=cols)

    print("Criando figura")
    fig = px.choropleth(
        finalDF,
        locations="Municipio",
        geojson=mp,
        featureidkey="properties.NOME",
        locationmode='geojson-id',
        animation_frame=cols[1],
        color="Value",
        title=f"{titleStr[typeIndex]}"
    )
    print("Figura criada")

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    print("Salvando figura")
    fig.show()
    fig.write_html(outputPath[typeIndex] + year + '.html')
    print("Sucesso...")