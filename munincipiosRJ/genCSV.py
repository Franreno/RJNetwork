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
    city = city + ", Rio de Janeiro"
    geolocator = Nominatim(user_agent="My-App")
    location = geolocator.geocode(city)
    lat,lng = location.latitude, location.longitude
    print(f"City: {city}: ({lat},{lng})")

    return [lat,lng]

def getDengueData():
    names = ['id', 'cities']
    for i in range(1,53):
        names.append(str(i))
    names.append('total')


    xlsPath = './munincipiosRJ/RJdata/Dengue_Brasil_2010-2016_Daniel.xlsx'
    df = pd.read_excel(xlsPath, names=names, header=None, sheet_name=None)
    sheets = list(df.keys())

    return df['2015']['total']


def main():
    limpath = './munincipiosRJ/RJdata/limitrofes.csv'
    LatLngPath = './munincipiosRJ/RJdata/LatLng.csv'
    limdf = pd.read_csv(limpath)
    limitrofes = {}


    LatLngDF = pd.read_csv(LatLngPath)

    allCities = getCities()
    allCitiesList = []

    DengueDataOfYear2015 = getDengueData()

    for i in range(len(limdf["Municipio"])):
        limitrofes[limdf["Municipio"][i]] = limdf["Municipios Limitrofes"][i]

    # Generate main list
    for i in range(len(allCities)):
        
        cityList = [allCities[i]]
        cityList.append(LatLngDF["Latitude"][i])
        cityList.append(LatLngDF["Longitude"][i])
        cityList.append(limitrofes[allCities[i]])
        cityList.append(DengueDataOfYear2015[i])
        allCitiesList.append(cityList)

    # Cols to be used in the pandas dataframe
    cols = ["Municipios", "Latitude", "Longitude", "Limitrofes", "TotalDengue"]
    df = pd.DataFrame(allCitiesList, columns=cols)
    df.to_csv('./munincipiosRJ/RJdata/mainRJData.csv')


# Create object to be used on the graph
def createListOfTuplesWithObject(dataframe):
    headTitles = ["id", "Municipio", "Latitude", "Longitude", "Limitrofes", "TotalDengue"]

    listOfTuples = []

    for i in range(len(dataframe)):
        #Create main object
        mainDict = {}
        mainDict[headTitles[1]] = dataframe["Municipios"][i]
        mainDict[headTitles[2]] = dataframe["Latitude"][i]
        mainDict[headTitles[3]] = dataframe["Longitude"][i]
        mainDict[headTitles[4]] = dataframe["Limitrofes"][i]
        mainDict[headTitles[5]] = dataframe["TotalDengue"][i]
        # distanceDict = (dataframe["Distancias"][i])
        # mainDict[headTitles[5]] = distanceDict
        
        listOfTuples.append( (i,mainDict) )


    return listOfTuples



if __name__ == "__main__":
    # getDengueData()
    main()
