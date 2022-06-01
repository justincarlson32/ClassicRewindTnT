import csv
import json
from multiprocessing.reduction import duplicate

fileNames = ["wm_Kills.json", "wmTBC_Kills.json", "bene_Kills.json"]

killCounter = {}

#remove duplicate reports
killTimestamps = []

for name in fileNames:

    print("-----------------------" + name)

    f = open(name)

    js = json.load(f)

    keys = list(js.keys())
    
    for i in range(1, int(max(keys)) + 1):
        for report in js[str(i)]['reportData']['reports']['data']:
    #try:
            encs = report['fights']
            startTime = report['startTime']
            for encID in encs:
               endTime = encID['endTime']
               isDuplciateReport = False
               for timeStamp in killTimestamps:
                   if (abs(timeStamp - (startTime + endTime)) < 300000):
                       print("duplicate report found")
                       isDuplciateReport = True

               if (isDuplciateReport == False):
                if encID['encounterID'] in killCounter.keys():
                   killCounter[encID['encounterID']] += 1
                else:
                   killCounter[encID['encounterID']] = 1
                killTimestamps.append(startTime + endTime)     

    #except:
    #    print(wipe)

encWipes = {}

for enc in killCounter.keys():
    with open("dungeonencounter.csv", "r") as read_file:
        data = csv.reader(read_file)
        for row in data:      
            if row[1] != 'ID' and int(row[1]) == int(enc):
                encWipes[row[0]] = killCounter[enc]


print(encWipes)

totalKills = 0

for enc in encWipes.keys():
    totalKills += encWipes[enc] 
print(totalKills)