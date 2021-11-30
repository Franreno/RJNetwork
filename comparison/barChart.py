import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from data import getData
IBGEDICT, UFRJDICT = getData()

years = ["2010", "2011", "2012"]

cities = list(IBGEDICT["2010"].keys())

fig = make_subplots(rows=92, cols=1, subplot_titles=cities)

for i in range(len(cities)):
    city = cities[i]
    ibge = []
    ufrj = []
    for j in range(len(years)):
        year = years[j]
        ibge.append(IBGEDICT[year][city])
        ufrj.append(UFRJDICT[year][city])

    fig.add_trace(go.Bar(x=years, y=ufrj, name="UFRJ", text=ufrj), row=i+1, col=1)
    fig.add_trace(go.Bar(x=years, y=ibge, name="IBGE", text=ibge), row=i+1, col=1)

fig['layout'].update(showlegend=False, height=25000, width=1200)


outputPath = "./plotlyPages/comparision/"
print("Salvando figura")
fig.show()
fig.write_html(outputPath + "Bar" + '.html')
print("Sucesso...")