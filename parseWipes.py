import csv
import json

fileNames = ["wipes_Wm.json", "wipes_WmTBC.json", "wipes_Bene.json"]

    
wipeCounter = {}

wipeTimestamps = []

for name in fileNames:

    print("-----------------------" + name)

    f = open(name)

    js = json.load(f)

    keys = list(js.keys())

    for i in range(1, int(max(keys)) + 1):
        for wipe in js[str(i)]['reportData']['reports']['data']:
    #try:
            encs = wipe['fights']
            startTime = wipe['startTime']
            for encID in encs:
               endTime = encID['endTime']
               isDuplciateReport = False
               for timeStamp in wipeTimestamps:
                   if (abs(timeStamp - (startTime + endTime)) < 300000):
                       print("duplicate report found")
                       isDuplciateReport = True

               if (isDuplciateReport == False):
                if encID['encounterID'] in wipeCounter.keys():
                   wipeCounter[encID['encounterID']] += 1
                else:
                   wipeCounter[encID['encounterID']] = 1
                wipeTimestamps.append(startTime + endTime)      

    #except:
    #    print(wipe)

encWipes = {}

for enc in wipeCounter.keys():
    with open("dungeonencounter.csv", "r") as read_file:
        data = csv.reader(read_file)
        for row in data:      
            if row[1] != 'ID' and int(row[1]) == int(enc):
                encWipes[row[0]] = wipeCounter[enc]


print(encWipes)

totalKills = 0

for enc in encWipes.keys():
    totalKills += encWipes[enc] 
print(totalKills)