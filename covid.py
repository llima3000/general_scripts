#!/usr/bin/env python3
import requests
import csv
import os
import pathlib
import datetime

path = "/tmp/"

days = 7
countryList = [ 
                'canada',
                'france',
                'spain',
                'portugal',
                'italy',
                'brazil',
                'uk',
]

# Function to downloas the csv file from the source
def getFileFromWeb():
    r = requests.get('https://hgis.uw.edu/virus/assets/virus.csv')

    if r.status_code == 200:
        print(r.headers['content-type'])
        print(r.encoding)
        data = csv.DictReader(r.text)
        f = open(path + "covid.csv","w")
        f.write(r.text)
        f.close()



dictCountrylist = dict()
for country in countryList:
    dictCountrylist[country] = []

if os.path.isfile(path + "covid.csv"):
    fname = pathlib.Path(path + "covid.csv")

    now = datetime.datetime.now()
    ctime = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
    print("Actual time: " + str(now))
    print("File " + str (now-ctime) + " old")
    if (now-ctime) > datetime.timedelta(hours=2):
        print("Getting new file version...")
        getFileFromWeb()
else:
    getFileFromWeb()

print()

with open(path + 'covid.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    last = 0
    for row in reader:
        for country in countryList:
            if row[country].__len__() > 0:
                dictCountrylist[country].append({"date": row['datetime'], "data": row[country].split('-')})

for country in countryList:
    print(country)
    last = 0
    lastdeath = 0
    for item in dictCountrylist[country][-days:]:
        strResp = item['date'] + " "
        strResp += str(int(item['data'][0])-last) + " "
        try:
            death = int(item['data'][3])
        except:
            death = 0

        strResp += str(death-lastdeath)

        #print(item['date'], int(item['data'][0])-last)
        print(strResp)
        last = int(item['data'][0])
        lastdeath = death

    print("Total: " + dictCountrylist[country][-1]['data'][0], dictCountrylist[country][-1]['data'][3], "(" + str(int(dictCountrylist[country][-1]['data'][3])/int(dictCountrylist[country][-1]['data'][0])*100) +")")
    print()
