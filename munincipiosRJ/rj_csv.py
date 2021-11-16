# Geopy for coordinates and distances
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# Pandas to read cities names
import pandas as pd
import numpy as np


from dataPath import *

names = ['id', 'cities']
for i in range(1, 53):
    names.append(str(i))
names.append('total')


# Get all cities names
def getCitiesAndPopulation():
    df = pd.read_excel(dadosMunicipiosRJ)
    return df["Município"], df["População_estimada_pessoas"]


def getDengueData(year):
    df = pd.read_excel(xlsDenguePath, names=names,
                       header=None, sheet_name=None)
    return df[year]['total']


def setupLimitrofes_Dict(limdf):
    d = {}
    for i in range(len(limdf["Municipio"])):
        d[limdf["Municipio"][i]] = limdf["Municipios Limitrofes"][i]
    return d


def setupLatLng_Dict(lldf):
    d = {}
    for i in range(len(lldf["Municipio"])):
        d[lldf["Municipio"][i]] = [
            lldf["Latitude"][i], lldf["Longitude"][i]]
    return d


def main():
    limitrofes_DF = pd.read_csv(limpath)
    LatLng_DF = pd.read_csv(LatLngPath)

    limitrofes_Dict = setupLimitrofes_Dict(limitrofes_DF)
    LatLng_Dict = setupLatLng_Dict(LatLng_DF)
    allCities, Population = getCitiesAndPopulation()

    allCities_List = []

    years = ['2010', '2011', '2012', '2013', '2014', '2015']
    DengueDataOfYear = [getDengueData(a) for a in years]

    # Generate main list
    for i in range(len(allCities)):
        cityList = [allCities[i]]
        cityList.append(LatLng_Dict[allCities[i]][0])
        cityList.append(LatLng_Dict[allCities[i]][1])
        cityList.append(limitrofes_Dict[allCities[i]])
        cityList.append(Population[i])
        for j in range(len(years)):
            cityList.append(DengueDataOfYear[j][i])

        allCities_List.append(cityList)

    # Cols to be used in the pandas dataframe
    cols = ["Municipios", "Latitude", "Longitude", "Limitrofes", "Populacao"]
    cols += years
    df = pd.DataFrame(allCities_List, columns=cols)
    df.to_csv('./RJdata/mainRJData.csv')


def normalize(df):
    result = df.copy()
    years = ["2010", "2011", "2012", "2013", "2014", "2015"]
    for year in years:
        result[year] = np.log(df[year])
    return result

# Create object to be used on the graph


def createListOfTuplesWithObject():

    df = pd.read_csv(mainRJDatapath)

    dataframe = normalize(df)

    years = ["2010", "2011", "2012", "2013", "2014", "2015"]
    headTitles = ["id", "Municipio", "Latitude", "Longitude", "Limitrofes", "Populacao"]
    headTitles += years

    listOfTuples = []

    for i in range(len(dataframe)):
        # Create main object
        mainDict = {}
        mainDict[headTitles[1]] = dataframe["Municipios"][i]
        mainDict[headTitles[2]] = dataframe["Latitude"][i]
        mainDict[headTitles[3]] = dataframe["Longitude"][i]
        mainDict[headTitles[4]] = dataframe["Limitrofes"][i]
        mainDict[headTitles[5]] = dataframe["Populacao"][i]
        mainDict[headTitles[6]] = dataframe["2010"][i]
        mainDict[headTitles[7]] = dataframe["2011"][i]
        mainDict[headTitles[8]] = dataframe["2012"][i]
        mainDict[headTitles[9]] = dataframe["2013"][i]
        mainDict[headTitles[10]] = dataframe["2014"][i]
        mainDict[headTitles[11]] = dataframe["2015"][i]

        listOfTuples.append((i, mainDict))

    return listOfTuples


if __name__ == "__main__":
    main()
