from bs4 import BeautifulSoup
import requests
import pandas as pd

def getAllLimitrofes():
    retObj = []
    mainurl = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Rio_de_Janeiro_por_popula%C3%A7%C3%A3o"

    htmlcontent = requests.get(mainurl).text

    bs4obj = BeautifulSoup(htmlcontent, 'html.parser')


    table = bs4obj.find("table")
    i=1
    for a in table.find_all("a"):
        aURL = a.get("href")
        if( ".svg" not in aURL and "Ficheiro" not in aURL):
            retObj.append(getLimitrofesFromCity(aURL))
            print(f"{i}/92")
            i+=1

    return retObj


def getLimitrofesFromCity(url):
    retObj = []

    preURL = "https://pt.wikipedia.org"
    cityURL = preURL + url 

    htmlcontent = requests.get(cityURL).text

    bs4obj = BeautifulSoup(htmlcontent, 'html.parser')

    
    title = bs4obj.find("h1")
    print(title.text)
    if ( "(" in title.text ):
        toAppend = title.text.replace(" (Rio de Janeiro)", "")
        retObj.append(toAppend)
    else:
        retObj.append(title.text)
        

    preflag = False
    limitrofeSTR = str()
    for td in bs4obj.find_all("td"):
        if(preflag):
            limitrofeSTR = td.text
            break
        if( td.text == "Municípios limítrofes\n" ):
            preflag = True


    rawLimitrofeList = limitrofeSTR.replace("\n", "").split(',')

    # Get last index cities that are in RJ
    lastIndex = len(rawLimitrofeList) - 1
    rawLimitrofeList[lastIndex] = rawLimitrofeList[lastIndex].split(" e ")

    lastElementCities = []
    for city in rawLimitrofeList[lastIndex]:
        if( "(" not in city and ")" not in city):
            lastElementCities.append(city)

    rawLimitrofeList.pop()
    
    for e in lastElementCities:
        rawLimitrofeList.append(e)


    # Remove cities that are not in RJ
    realLimitrofesCities = []
    for city in rawLimitrofeList:
        if( "(" not in city and ")" not in city):
            realLimitrofesCities.append(city)

    #check for empty strings
    for i in range(len(realLimitrofesCities)-1):
        if not realLimitrofesCities[i]:
            realLimitrofesCities.pop(i)

    #Remove space in first position
    for i in range(len(realLimitrofesCities)):
        if(realLimitrofesCities[i][0] == " "):
            realLimitrofesCities[i] = realLimitrofesCities[i][1:]
            
    #Concatenate back to a string
    retStr = ','.join(realLimitrofesCities)
        
    retObj.append(retStr)
    return retObj

def parseAndCreateCSV(obj):
    cols = ["Municipios", "Municipios Limitrofes"]
    df = pd.DataFrame(obj, columns=cols)
    df.to_csv('limitrofes.csv')


if __name__ == "__main__":
    parseAndCreateCSV(getAllLimitrofes())    



