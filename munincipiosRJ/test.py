from genGraph import createNetwork
import networkx as nx
import plotly.graph_objects as go
import numpy as np

G = createNetwork()
weeks = np.linspace(0, 51, 51, dtype=int)

# Colocar os nós como se fosse no rio de janeiro
# Misturar os dados de dengue.

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['data'].lngLat
    x1, y1 = G.nodes[edge[1]]['data'].lngLat
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['data'].lngLat
    node_x.append(x)
    node_y.append(y)

#------------------------------#

years = ["2010", "2011", "2012", "2013", "2014", "2015"]
year = "2010"

figDict = dict(
    # data=[],
    layout=dict(),
    frames=[]
)

slider = dict(
    active=0,
    yanchor="top",
    xanchor="left",
    currentvalue=dict(
        font=dict(size=20),
        prefix="Semana: ",
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


def createNodeTrace(year, index):
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Rainbow',
            reversescale=False,
            color=[],
            size=10,
            colorbar=dict(
                thickness=10,
                title=f'Total de casos de Dengue no ano',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies, node_text = nodeMarkerAndText(year, index)
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    return node_trace



def nodeMarkerAndText(year, week):
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        # Add new data from week[week]
        newData = G.nodes[node]['data'].dengueData[year][week]
        G.nodes[node]['data'].dengueDataCumulative += newData
        if newData != 0:
            newData = np.log10(newData)

        G.nodes[node]['data'].logDengueDataCumulative += newData

        node_adjacencies.append(
            G.nodes[node]['data'].logDengueDataCumulative)
        node_text.append(f"Municipio: {G.nodes[node]['data'].city}[{str(node)}]  |Casos de Dengue: { str(G.nodes[node]['data'].dengueDataCumulative) }")

    return node_adjacencies, node_text


titleStr = f"Casos de dengue ao longo do ano de {year}."
figDict["layout"]["xaxis"] = dict(showgrid=False, zeroline=False,showticklabels=False)
figDict["layout"]["yaxis"] = dict(showgrid=False, zeroline=False, showticklabels=False)
figDict["layout"]["hovermode"] = "closest"
figDict["layout"]["showlegend"] = False
figDict["layout"]["title"] = titleStr

playButton = dict(
    args= [
        None,
        dict(
            frame=dict(duration=500, redraw=False),
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

figDict["layout"]["sliders"] = [slider]


nodeTraces = {}
for week in weeks:
    nodeTraces[week] = createNodeTrace(year , week)

figDict["data"] = [edge_trace, nodeTraces[0]]

for week in weeks:
    frame = dict(
        data=[edge_trace, nodeTraces[week]],
        name=str(week)
    )
    figDict["frames"].append(frame)

    slider_step = dict(
        args = [
            [week+1],
            dict(
                frame=dict(duration=300, redraw=False),
                mode="immediate",
                transition=dict(duration=300)
            )
        ],
        label=str(week+1),
        method="animate"
    )
    slider["steps"].append(slider_step)



figDict["layout"]["sliders"] = [slider]

fig = go.Figure(figDict)

fig.show()
