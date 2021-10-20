import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from genCSV import createListOfTuplesWithObject


def createNetwork():

    data = createListOfTuplesWithObject()

    G = nx.Graph()

    # Add nodes
    for i in range(len(data)):
        G.add_nodes_from([(i, data[i][1])])

    # Generate random positions
    # pos = nx.drawing.layout.random_layout(G)
    # Add to the nodes data

    i = 0
    for node in G.nodes:
        G.nodes[node]['gpos'] = (data[i][1]['Longitude'], data[i][1]['Latitude'])
        i += 1

    # Add edges
    for i in range(len(data)):
        cityNumber = data[i][0]
        cityName = data[i][1]["Municipio"]
        limitrofes = data[i][1]["Limitrofes"].split(',')

        for l in limitrofes:
            # Search the data for l
            for j in range(len(data)):
                if (l == data[j][1]["Municipio"]):
                    newEdge = data[j][0]

                    G.add_edge(cityNumber, newEdge)

    return G


# G = createNetwork()
# pos = {city:(long,lat) for (city, (long, lat)) in nx.get_node_attributes(G, 'gpos').items()}
# nx.draw(G,pos,with_labels=True, font_weight='bold')
# plt.show()
