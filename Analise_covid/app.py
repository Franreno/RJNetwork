import plotly.express as px
import numpy as pd
import pandas as pd
import matplotlib.pyplot as plt
import json


covidDataPath = "./Analise_covid/Data/cases-brazil-cities-time.csv"
estadosPath = "./Analise_covid/Data/estados.csv"
municipiosPath = "./Analise_covid/Data/municipios.csv"
jsonPath = "./Analise_covid/Data/geojs-100-mun.json"
with open(jsonPath, "r") as geo:
    mp = json.load(geo)

# Create map with data
estadosDF = pd.read_csv(estadosPath)

covidData = pd.read_csv( covidDataPath )

#Remover o total e casos nao definidos
covidData = covidData[ ['ibgeID', 'date', 'totalCases', 'city', 'state'] ]
covidData = covidData[covidData.city != "TOTAL"]
covidData = covidData[~covidData.city.astype(str).str.startswith("CASO SEM LOCALIZAÇÃO DEFINIDA")]
covidData = covidData[covidData.date.astype(str).str.endswith("01")]

# Sort by date
covidData = covidData.sort_values("date")

#Remover o /UF
covidData["city"] = covidData["city"].apply( lambda x: x[:-3] )


capitais_estados = ["Porto Velho", "Manaus", "Rio Branco", "Campo Grande", "Macapá", "Brasília", "Boa Vista", "Cuiabá", "Palmas", "São Paulo", "Teresina", "Rio de Janeiro", "Belém", "Goiânia", "Salvador", "Florianópolis", "São Luís", "Maceió", "Porto Alegre", "Curitiba", "Belo Horizonte", "Fortaleza", "Recife", "João Pessoa", "Aracaju", "Natal", "Vitória"]

#Remover as capitais dos estados
for capital in capitais_estados:
    covidData = covidData[ covidData.city != capital ]

for UF_TO_ANIMATE, UF_NAME in zip(estadosDF["SIGLA"], estadosDF["NOME"]):
    UF_TO_ANIMATE = UF_TO_ANIMATE.replace(" ", "")
    print(f"Fazendo para {UF_TO_ANIMATE}")

    dataframe_to_animate = covidData[covidData.state == UF_TO_ANIMATE]

    colorValues = ['rgb(0, 0, 255)', 'rgb(75, 0, 130)', 'rgb(238, 130, 238)', 'rgb(255, 0, 0)', 'rgb(255, 165, 0)', 'rgb(255, 255, 0)', 'rgb(0, 128, 0)']

    colorScale = [ [0.0, colorValues[0]] ]
    colorScale.append( [0.3, colorValues[1]] )
    colorScale.append( [0.5, colorValues[2]] )
    colorScale.append( [0.7, colorValues[3]] )
    colorScale.append( [0.9, colorValues[4]] )
    colorScale.append( [0.995, colorValues[5]] )
    colorScale.append( [1, colorValues[6]] )

    print("Criando figura")
    fig = px.choropleth(
        dataframe_to_animate,
        locations="ibgeID",
        geojson=mp,
        featureidkey="properties.id",
        locationmode='geojson-id',
        animation_frame="date",
        color="totalCases",
        hover_data=["city"],
        title=f"Casos de covid-19 no Brasil no estado {UF_NAME}",
        # color_continuous_scale=colorScale
    )
    print("Figura criada")

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    outputPath = "./plotlyPages/covid/"
    print("Salvando figura")
    fig.show()
    fig.write_html(outputPath + UF_TO_ANIMATE + '.html')
    print("Sucesso...")
