from genGraph import createNetwork
import networkx as nx
import plotly.graph_objects as go

G = createNetwork()


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

# years = input("Escolha um ano: [2010, 2011, 2012, 2013, 2014, 2015]\n  >")
# year = year if year != None else "2010"
# years = ["2010", "2011", "2012", "2013", "2014", "2015"]
years = ["2010"]
for year in years:
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=f'Total de casos de Dengue no ano {year}',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append( G.nodes[node]['data'].totalYearDengueData[0] )
        node_text.append(f"Municipio: {G.nodes[node]['data'].city}[{str(node)}]   |   Total de casos de Dengue no Ano {year}: { str(G.nodes[node]['data'].totalYearDengueData[0]) }")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=f'<br>Grafo Rio de Janeiro. Ano {year}',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.update_xaxes(rangeslider_visible=True)

    fig.show()