import requests
import time
from bs4 import BeautifulSoup

#  'Aransas+Pass',  'Sabine+Lake', not for every year

# and then apparently does not work for 2020?... or atleast bolivar
locationsList = [
    'East+Matagorda+Bay',
    'Baffin+Bay',
    'Bolivar',
    'Corpus+Christi',
    'East+Galveston+Bay',
    'Freeport',
    'North+Sabine',
    'Port+Aransas',
    'Port+Isabel',
    'Port+Mansfield',
    'Port+O%27Connor',
    'Rockport',
    'South+Padre',
    'South+Sabine',
    'Texas+City',
    'Trinity+Bay',
    'West+Galveston+Bay',
    'West+Matagorda+Bay'
]

Years = ['2010',
'2011',
'2012',
'2013',
'2014',
'2015',
'2016',
'2017',
'2018',
'2019',
'2020']

class Report:
    def __init__(self, date, location, highlights):
        self._date = date
        self._location = location
        self._highlights = highlights

    def printTable(self):
        for h in self._highlights:
            print(self._date + '--' + self._location + '--' + h)

fakeYears = ['2020']

for y in fakeYears:
    for locz in locationsList:
        #https://tpwd.texas.gov/fishboat/fish/action/reptform2.php?lake=Bolivar&archive=wholeyear&yearcat=2020&Submit=View+Report
        URL = 'https://tpwd.texas.gov/fishboat/fish/action/reptform2.php?lake='+locz+'&archive=wholeyear&yearcat='+y+'&Submit=View+Report'

        if ((locz == 'Bolivar' and y == '2020') or (locz == 'North+Sabine' and y == '2020') or (locz == 'South+Sabine' and y == '2020')):
            continue

        print(y)
        print(locz)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        interest = soup.find('dl')
        dt = interest.find('dt')
        title = dt.find('span', {'class': 'title'})
        titleText = title.get_text()

        #print(interest)
        # print('------')
        # print(dt)
        # print('------')
        # print(title)
        # print('------')
        # print(titleText)

        print('------')
        print('------')
        print('------')
        print('------')

        allDates = interest.find_all('dt')
        allDescriptions = interest.find_all('dd')

        reportList = []

        for dt in allDates:
            #gets the date value
            myDate = dt.find('span', {'class': 'title'}).get_text()

            #creates and cleans the list of descriptions on what is effective
            desc = dt.findNext('dd').get_text()
            descList = desc.split('.')
            descList = [h.strip(' ') for h in descList]

            prettyLoc = locz.replace('+', ' ')
            prettyLoc = locz.replace('%27', '\'')

            #creates the report object, and appends it to the list that will be appended to the report list
            report = Report(myDate, prettyLoc, descList)
            reportList.append((report))

        #Just for proof that we can create a row the way we need
        firstRep = reportList[0]
        firstRep.printTable()
        time.sleep(2)



#saltwater locations:
#https://tpwd.texas.gov/fishboat/fish/action/reptform2.php?lake=East+Matagorda+Bay&archive=wholeyear&yearcat=2019&Submit=View+Report


# for desc in allDescriptions:
#     descList.append(desc)
#     print(desc.get_text())
#
# print('------')
#
# firstDesc = str(descList[0])
# firstDescList = firstDesc.split('.')
#
# firstDescList[0] = firstDescList[0].replace('<dd>', '')
# firstDescList[-1] = firstDescList[-1].replace('</dd>', 'End of Desc')
#
# print('---first one ---')
# print(firstDescList[0].replace('<dd>', ''))
# print(firstDescList[-1].replace('</dd>', ''))
# print('---last one ---')
#
# for part in firstDescList:
#     print(part)


#Seems like fair, fair to good, good, very good, excellent.... picked up?







