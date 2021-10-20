# Geopy for coordinates and distances
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# Pandas to read cities names
import pandas as pd
import numpy as np


dadosMunicipiosRJ = './munincipiosRJ/RJdata/dadosMunicipiosRJ.xlsx'

# Get all cities names
def getCities(): 
    df = pd.read_excel(dadosMunicipiosRJ)
    allCities = df["Município"]
    return allCities

# Calculate all distances from a certain city
def calculateDistances(currentCity: str, latlnglist):
    geolocator = Nominatim(user_agent="My-App")
    _thisCity = [currentCity]
    _thisDict = {}

    # get lat and lng for current city
    currentCityLocation = geolocator.geocode(currentCity)
    currentCityLat, currentCityLng = currentCityLocation.latitude, currentCityLocation.longitude

    for city in latlnglist:
        if (city == currentCity):
            _thisDict[city] = 0.0
            continue
        
        # print(f"\tGetting distance of city {city} to {currentCity}\n")
        lat,lng = latlnglist[city][0], latlnglist[city][1]
        _dist = geodesic( (currentCityLat, currentCityLng) , (lat, lng) )
        _thisDict[city] = _dist.km
        
    print("---------------------------------------------\n")
    _thisCity.append(_thisDict)
    return _thisCity

# Gets the latitude and longitude of a city  
def getLatLng(city):
    city = city + ", Rio de Janeiro"
    geolocator = Nominatim(user_agent="My-App")
    location = geolocator.geocode(city)
    lat,lng = location.latitude, location.longitude
    print(f"City: {city}: ({lat},{lng})")

    return [lat,lng]

def getDengueData(year):
    names = ['id', 'cities']
    for i in range(1,53):
        names.append(str(i))
    names.append('total')


    xlsPath = './munincipiosRJ/RJdata/Dengue_Brasil_2010-2016_Daniel.xlsx'
    df = pd.read_excel(xlsPath, names=names, header=None, sheet_name=None)
    sheets = list(df.keys())

    return df[year]['total']


def main():
    limpath = './munincipiosRJ/RJdata/limitrofes.csv'
    LatLngPath = './munincipiosRJ/RJdata/LatLng.csv'
    limdf = pd.read_csv(limpath)
    limitrofes = {}


    LatLngDF = pd.read_csv(LatLngPath)

    allCities = getCities()
    allCitiesList = []

    years = ['2010', '2011', '2012', '2013', '2014', '2015']

    DengueDataOfYear = [getDengueData(a) for a in years]
    

    for i in range(len(limdf["Municipio"])):
        limitrofes[limdf["Municipio"][i]] = limdf["Municipios Limitrofes"][i]

    # Generate main list
    for i in range(len(allCities)):
        
        cityList = [allCities[i]]
        cityList.append(LatLngDF["Latitude"][i])
        cityList.append(LatLngDF["Longitude"][i])
        cityList.append(limitrofes[allCities[i]])
        for j in range(len(years)):
            cityList.append(DengueDataOfYear[j][i])
        allCitiesList.append(cityList)

    # Cols to be used in the pandas dataframe
    cols = ["Municipios", "Latitude", "Longitude", "Limitrofes"]
    cols += years
    print(cols)
    df = pd.DataFrame(allCitiesList, columns=cols)
    df.to_csv('./munincipiosRJ/RJdata/mainRJData.csv')


def normalize(df):
    result = df.copy()
    years = ["2010", "2011", "2012", "2013", "2014", "2015"]
    for year in years:
        # max_value = df[year].max()
        # min_value = df[year].min()
        # result[year] = (df[year] - min_value) / (max_value - min_value)
        result[year] = np.log(df[year])
    return result

# Create object to be used on the graph
def createListOfTuplesWithObject():
    mainRJDatapath = './munincipiosRJ/RJdata/mainRJData.csv'

    df = pd.read_csv(mainRJDatapath)

    dataframe = normalize(df)


    headTitles = ["id", "Municipio", "Latitude", "Longitude", "Limitrofes", "2010", "2011", "2012", "2013", "2014", "2015"]


    listOfTuples = []

    for i in range(len(dataframe)):
        #Create main object
        mainDict = {}
        mainDict[headTitles[1]]  = dataframe["Municipios"][i]
        mainDict[headTitles[2]]  = dataframe["Latitude"][i]
        mainDict[headTitles[3]]  = dataframe["Longitude"][i]
        mainDict[headTitles[4]]  = dataframe["Limitrofes"][i]
        mainDict[headTitles[5]]  = dataframe["2010"][i]
        mainDict[headTitles[6]]  = dataframe["2011"][i]
        mainDict[headTitles[7]]  = dataframe["2012"][i]
        mainDict[headTitles[8]]  = dataframe["2013"][i]
        mainDict[headTitles[9]]  = dataframe["2014"][i]
        mainDict[headTitles[10]] = dataframe["2015"][i]
        # distanceDict = (dataframe["Distancias"][i])
        # mainDict[headTitles[5]] = distanceDict
        
        listOfTuples.append( (i,mainDict) )


    return listOfTuples



if __name__ == "__main__":
    # getDengueData()
    main()
