import numpy as np
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from data import getData

figDict = dict(
    data=[],
    layout=dict(),
    frames=[]
)

slider = dict(
    active=0,
    yanchor="top",
    xanchor="left",
    currentvalue=dict(
        font=dict(size=20),
        prefix="Cidade: ",
        visible=True,
        xanchor="right"
    ),
    transition=dict(duration=300, easing="cubic-in-out"),
    pad=dict(b=10,t=20),
    len=0.9,
    x=0.1,
    y=0,
    steps=[]
)

titleStr = "Comparação entre os dados da UFRJ e IBGE"
# figDict["layout"]["xaxis"] = dict(showgrid=False, zeroline=False,showticklabels=False)
# figDict["layout"]["yaxis"] = dict(showgrid=False, zeroline=False, showticklabels=False)
figDict["layout"]["hovermode"] = "closest"
figDict["layout"]["showlegend"] = False
figDict["layout"]["title"] = titleStr


playButton = dict(
    args= [
        None,
        dict(
            frame=dict(duration=250, redraw=False),
            fromcurrent=True,
            transition=dict(duration=300, easing= "quadratic-in-out")
        )
    ],
    label="Play",
    method="animate"
)

pauseButton = dict(
    args= [
        [None],
        dict(
            frame=dict(duration=0, redraw=False),
            mode="immediate",
            transition=dict(duration=0)
        )
    ],
    label="Pause",
    method="animate"
)

figDict["layout"]["updatemenus"] = [
    dict(
        buttons=[playButton, pauseButton],
        direction="left",
        pad=dict(r=10, t=87),
        showactive=True,
        type="buttons",
        x=0.1,
        xanchor="right",
        y=0,
        yanchor="top"
    )
]




IBGEDICT, UFRJDICT = getData()

# Get cities names
cities = list(IBGEDICT["2010"].keys())
years = ["2010", "2011", "2012"]

# Make data
dataList = []
for i in range(len(cities)):
    city = cities[i]
    ibgeData = []
    ufrjData = []
    for year in years:
        ibgeData.append( IBGEDICT[year][city] )
        ufrjData.append( UFRJDICT[year][city] )

    ibgeBar = go.Bar(x=years, y=ibgeData, name="IBGE", text=ibgeData)
    ufrjBar = go.Bar(x=years, y=ufrjData, name="UFRJ", text=ufrjData)
    dataList.append( [ibgeBar, ufrjBar] )

# figDict["data"] = dataList[0]

# Make frames

for i in range(0,len(dataList)):
    frame = dict(
        data=dataList[i],
        name=cities[i]
    )
    figDict["frames"].append(frame)

    slider_step = dict(
        args = [
            [cities[i]],
            dict(
                frame=dict(duration=300, redraw=False),
                mode="immediate",
                transition=dict(duration=300)
            )
        ],
        label=cities[i],
        method="animate"
    )
    slider["steps"].append(slider_step)


figDict["layout"]["sliders"] = [slider]
fig = go.Figure(figDict)
fig.show()
