import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

names = ['id', 'cities']
weeksToPlot = []
for i in range(1,53):
    names.append(str(i))
    weeksToPlot.append(i)
names.append('total')


dataset = pd.read_excel(r'Dengue_Brasil_2010-2016_Daniel.xlsx', names=names, header=None, sheet_name=None)
sheets = list(dataset.keys())

px = 1/plt.rcParams['figure.dpi']  # pixel in inches
for cityIterator in range(len(dataset['2010']['cities'])):
    print(f"Creating image for city[{cityIterator}]: " + dataset['2010']['cities'][cityIterator] + "\n")

    fig = plt.figure(figsize=(2048*px,1080*px))
    axis = fig.subplots(3,2)
    fig.suptitle(dataset['2010']['cities'][cityIterator])

    k = 0
    for i in range(3):
        for j in range(2):
            axis[i,j].plot( np.array((names[2:len(names)-1])), np.array(dataset[sheets[k]].loc[:, '1' : '52'].iloc[cityIterator]) )
            axis[i,j].set_title(sheets[k])
            k+=1
    plt.tight_layout()
    plt.savefig('figures/' + dataset['2010']['cities'][cityIterator])
    plt.close()


