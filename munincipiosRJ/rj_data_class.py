import pandas as pd

mainRJDatapath = './munincipiosRJ/RJdata/mainRJData.csv'


class rjData:
    def __init__(self):
        df = pd.read_csv(mainRJDatapath)
        self.years = ["2010", "2011", "2012", "2013", "2014", "2015"]
        self.headTitles = ["id", "Municipio", "Latitude",
                           "Longitude", "Limitrofes", "Populacao"]
        self.headTitles += self.years

        self.municipios = df["Municipios"]
        self.longitudes = df["Longitude"]
        self.latitudes = df["Latitude"]
        self.limitrofes = df["Limitrofes"]
        self.populacoes = df["Populacao"]
        self.dataFrom2010 = df["2010"]
        self.dataFrom2011 = df["2011"]
        self.dataFrom2012 = df["2012"]
        self.dataFrom2013 = df["2013"]
        self.dataFrom2014 = df["2014"]
        self.dataFrom2015 = df["2015"]

    def initializeNodeData(self):
        listOfObjects = []

        for i in range(len(self.municipios)):
            listOfObjects.append(
                rjDataNode(
                    self.municipios[i], self.longitudes[i], self.latitudes[i], self.limitrofes[i], self.populacoes[i],
                    self.dataFrom2010[i], self.dataFrom2011[i], self.dataFrom2012[i], self.dataFrom2013[i],
                    self.dataFrom2014[i], self.dataFrom2015[i]
                )
            )
        return listOfObjects


class rjDataNode(rjData):
    def addDengueDataOfYear(self, df):
        pass


    
    def __init__(self, city, lng, lat, limf, pop, d2010, d2011, d2012, d2013, d2014, d2015):
        self.city = city
        self.lngLat = [lng, lat]
        self.limitrofe = limf
        self.populacao = pop
        self.totalYearDengueData = [d2010, d2011, d2012, d2013, d2014, d2015]
        # super().__init__()

    def setCityName(self, name):
        self.city = name


# r = rjData()
# listOfNodes = r.initializeNodeData()
# print(listOfNodes[0])
