import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from rj_csv import createListOfTuplesWithObject
from rj_data_class import rjData, rjDataNode

def createNetwork():

    dataObjs = rjData().initializeNodeData()

    G = nx.Graph()

    # Add nodes
    for i in range(len(dataObjs)):
        # G.add_nodes_from
        # G.add_nodes_from( [ (i, data[i]) ] )
        G.add_node(i, data=dataObjs[i])

    # i = 0
    # for node in G.nodes:
    #     G.nodes[node]['gpos'] = (data[i][1]['Longitude'], data[i][1]['Latitude'])
    #     i += 1


    for i in range(len(dataObjs)):
        cityNumber = i
        limitrofes = dataObjs[i].limitrofe.split(',')
        # print(cityNumber, limitrofes)

        for l in limitrofes:
            for j in range(len(dataObjs)):
                if( l == dataObjs[j].city ):
                    # print(l, dataObjs[j].city)
                    newEdge = j
                    # print(cityNumber, newEdge)
                    G.add_edge(cityNumber, newEdge)

    return G


# G = createNetwork()
# pos = {}
# for node in G.nodes:
#     pos[node] = tuple(G.nodes[node]['data'].lngLat)

# nx.draw(G,pos,with_labels=True, font_weight='bold')
# plt.show()
