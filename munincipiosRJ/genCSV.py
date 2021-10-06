# Geopy for coordinates and distances
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# Pandas to read cities names
import pandas as pd

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
    geolocator = Nominatim(user_agent="My-App")
    location = geolocator.geocode(city)
    lat,lng = location.latitude, location.longitude

    return [lat,lng]

# Create object to be used on the graph
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
    limpath = './munincipiosRJ/RJdata/limitrofes.csv'
    limdf = pd.read_csv(limpath)

    allCities = getCities()
    allCitiesList = []
    latlnglist = {}

    # Generate lat,lng dict
    for i in range(len(allCities)):
        print(f"Getting lat and lng from city {i}/{len(allCities)}\n")
        latlnglist[allCities[i]] = getLatLng(allCities[i])

    # Generate main list
    for i in range(len(allCities)):
        print(f"Calculating distance from city {allCities[i]} -- {i}/{len(allCities)} . . .\n")
        cityList = calculateDistances(allCities[i], latlnglist)
        cityList.insert(1, limdf['Municipios Limitrofes'][i])
        cityList.insert(1, latlnglist[allCities[i]][1])
        cityList.insert(1, latlnglist[allCities[i]][0])
        allCitiesList.append(cityList)

    # Cols to be used in the pandas dataframe
    cols = ["Municipios", "Latitude", "Longitude", "Limitrofes", "Distancias"]
    df = pd.DataFrame(allCitiesList, columns=cols)
    df.to_csv('./munincipiosRJ/RJdata/mainRJData.csv')



if __name__ == "__main__":
    main()
