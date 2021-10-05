# Geopy for coordinates and distances
from geopy import distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# Pandas to read cities names
import pandas as pd
import ast

dadosMunicipiosRJ = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/dadosMunicipiosRJ.xlsx'

def getCities(): 
    df = pd.read_excel(dadosMunicipiosRJ)
    allCities = df["Município"]
    return allCities

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
        
    
def getLatLng(city):
    geolocator = Nominatim(user_agent="My-App")
    location = geolocator.geocode(city)
    lat,lng = location.latitude, location.longitude

    return [lat,lng]

def createListOfTuplesWithObject(dataframe):
    headTitles = ["id", "Municipio", "Latitude", "Longitude", "Limitrofes", "Distancia"]

    listOfTuples = []

    for i in range(len(dataframe)):
        #Create main object
        mainDict = {}
        mainDict[headTitles[1]] = dataframe["Municipios"][i]
        mainDict[headTitles[2]] = dataframe["Latitude"][i]
        mainDict[headTitles[3]] = dataframe["Longitude"][i]
        mainDict[headTitles[4]] = dataframe["Limitrofes"][i]
        distanceDict = (dataframe["Distancias"][i])
        mainDict[headTitles[5]] = distanceDict
        
        listOfTuples.append( (i,mainDict) )


    return listOfTuples

def main():
    limpath = '/home/franreno/Documents/ic/munincipiosRJ/RJdata/limitrofes.csv'
    limdf = pd.read_csv(limpath)

    allCities = getCities()
    allCitiesList = []
    latlnglist = {}
    for i in range(len(allCities)):
        print(f"Get lat and lng from city {i}/{len(allCities)}\n")
        latlnglist[allCities[i]] = getLatLng(allCities[i])

    for i in range(len(allCities)):
        print(f"Calculating distance from city {allCities[i]} -- {i}/{len(allCities)} . . .\n")
        cityList = calculateDistances(allCities[i], latlnglist)
        cityList.insert(1, limdf['Municipios Limitrofes'][i])
        cityList.insert(1, latlnglist[allCities[i]][1])
        cityList.insert(1, latlnglist[allCities[i]][0])
        allCitiesList.append(cityList)

    cols = ["Municipios", "Latitude", "Longitude", "Limitrofes", "Distancias"]
    df = pd.DataFrame(allCitiesList, columns=cols)
    df.to_csv('distanciasRJ.csv')

if __name__ == "__main__":
    main()
