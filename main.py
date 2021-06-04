import pymysql
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

#  'Aransas+Pass',  'Sabine+Lake', not for every year

# and then apparently does not work for 2020?... or atleast bolivar
# locationsList = [
#     'East+Matagorda+Bay',
#     'Baffin+Bay',
#     'Bolivar',
#     'Corpus+Christi',
#     'East+Galveston+Bay',
#     'Freeport',
#     'North+Sabine',
#     'Port+Aransas',
#     'Port+Isabel',
#     'Port+Mansfield',
#     'Port+O%27Connor',
#     'Rockport',
#     'South+Padre',
#     'South+Sabine',
#     'Texas+City',
#     'Trinity+Bay',
#     'West+Galveston+Bay',
#     'West+Matagorda+Bay'
# ]

locationsDict = {
'East Matagora Bay':'East+Matagorda+Bay',
'Baffin Bay':'Baffin+Bay',
'Bolivar': 'Bolivar',
'Corpus Christi':'Corpus+Christi',
'East Galveston Bay':'East+Galveston+Bay',
'Freeport':'Freeport',
'North Sabine':'North+Sabine',
'Port Aransas':'Port+Aransas',
'Port Isabel':'Port+Isabel',
'Port Mansfield':'Port+Mansfield',
'Port O\'Conner':'Port+O%27Connor',
'Rockport':'Rockport',
'South Padre':'South+Padre',
'South Sabine':'South+Sabine',
'Texas City':'Texas+City',
'Trinity Bay':'Trinity+Bay',
'West Galveston Bay':'West+Galveston+Bay',
'West Matagorda Bay':'West+Matagorda+Bay'
}

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

    def __init__(self, date, location, sentences, paragraph):
        self._date = date
        self._location = location
        self._sentences = sentences
        self._paragraph = paragraph
        self._redfish = ''
        self._trout = ''
        self._flounder = ''

    def printTable(self):
        for h in self._sentences:
            if ('reds' in h
                    or 'redfish' in h
                    or 'Redfish' in h
                    or 'red drum' in h
                    or 'Reds' in h
                    or 'Red drum' in h):
                self._redfish = self._redfish + ':' + h
                #print("h has reds: " + h)
            if ('trout' in h
                    or 'Trout' in h
                    or 'Speckled' in h
                    or 'Specs' in h):
                self._trout = self._trout + ':' + h
                #print("h has specs: " + h)
            if ('Flounder' in h or 'flounder' in h):
                self._flounder = self._flounder + ':' + h
                #print("h has flounder: " + h)
        print(str(self._date) + '--' + self._location + '--R' + self._redfish + '--T' + self._trout + '--F' +
              self._flounder + '--' + self._paragraph)

    def insertTable(self):
        conn = pymysql.connect(host='hiding for security', user='hidden', passwd='hidden',
                                db='hidden')
        cursor = conn.cursor()

        for h in self._sentences:
            # insertStatement = 'INSERT INTO TPWLFishingReport (ReportDate, Area, Sentence) VALUES (%s, %s, %s)'
            # cursor.execute(insertStatement, (self._date, self._location, h))

            if ('reds' in h
                    or 'redfish' in h
                    or 'Redfish' in h
                    or 'red drum' in h
                    or 'Reds' in h
                    or 'Red drum' in h):
                #self._redfish = self._redfish + ':' + h
                self._redfish.join([self._redfish, h])
                # print("h has reds: " + h)
            if ('trout' in h
                    or 'Trout' in h
                    or 'Speckled' in h
                    or 'Specs' in h):
                #self._trout = self._trout + ':' + h
                self._trout.join(([self._trout, h]))
                # print("h has specs: " + h)
            if ('Flounder' in h or 'flounder' in h):
                self._flounder.join([self._flounder, h])
                #self._flounder = self._flounder + ':' + h
                # print("h has flounder: " + h)
        #print(str(self._date) + '--' + self._location + '--R' + self._redfish + '--T' + self._trout + '--F' +
         #     self._flounder + '--' + self._paragraph)

        now = datetime.now()

        insertStatement = 'INSERT INTO TPWLFishingReport (CreationDatetime, ReportDate, Area, Redfish, Trout, Flounder, Paragraph) ' \
                          'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(insertStatement, (now, self._date, self._location, self._redfish, self._trout, self._flounder, self._paragraph))

        conn.commit()
        conn.close()


fakeYears = ['2020']

for y in Years:
    for key, value in locationsDict.items():
        #https://tpwd.texas.gov/fishboat/fish/action/reptform2.php?lake=Bolivar&archive=wholeyear&yearcat=2020&Submit=View+Report
        URL = 'https://tpwd.texas.gov/fishboat/fish/action/reptform2.php?lake='+value+'&archive=wholeyear&yearcat='+y+'&Submit=View+Report'

        if ((value == 'Bolivar' and y == '2020') or (value == 'North+Sabine' and y == '2020') or (value == 'South+Sabine' and y == '2020')):
            continue

        #print(y)
        #print(value)
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

        allDates = interest.find_all('dt')
        allDescriptions = interest.find_all('dd')

        reportList = []

        for dt in allDates:
            #gets the date value
            myDate = dt.find('span', {'class': 'title'}).get_text()
            myDate = myDate.replace(",","")
            #print(myDate)
            reportDate = datetime.strptime(myDate, '%b %d %Y')
            #print(reportDate)

            #creates and cleans the list of descriptions on what is effective
            desc = dt.findNext('dd').get_text()
            descList = desc.split('.')
            descList = [h.strip(' ') for h in descList]

            # prettyLoc = value.replace('+', ' ')
            # prettyLoc = value.replace('%27', '\'')

            #creates the report object, and appends it to the list that will be appended to the report list
            report = Report(reportDate, key, descList, desc)
            reportList.append((report))

        #Just for proof that we can create a row the way we need
        firstRep = reportList[0]
        firstRep.printTable()
        firstRep.insertTable()
        print('------')
        print('------')
        print('------')
        print('------')
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


#for key, value in locationsDict.items():
 #   print(key, value)






