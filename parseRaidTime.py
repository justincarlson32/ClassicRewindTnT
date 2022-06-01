import csv
import json
from turtle import pen

fileNames = ["Wm_raidTime.json", "WmTBC_raidTime.json", "bene_raidTime.json"]

startTimes = []
endTimes = []

for name in fileNames:

    print("-----------------------" + name)

    totalTime = 0

    f = open(name)

    js = json.load(f)

    keys = list(js.keys())
    

    for i in range(1, int(max(keys)) + 1):
        for report in js[str(i)]['reportData']['reports']['data']:
            startTime = int(report['startTime'])
            endTime = int(report['endTime'])

            isDuplciateReport = False
            for timeStamp in startTimes:
                if (abs(startTime - timeStamp) < 300000):
                    isDuplciateReport = True
                
            for endtimeStamp in endTimes:
                if (abs(endTime - endtimeStamp) < 300000):
                    isDuplciateReport = True
                
            if (isDuplciateReport == True):
                continue

            startTimes.append(startTime)
            endTimes.append(endTime)            
            totalTime += report['endTime'] - report['startTime']

    print(totalTime)

    print("-------------------------end")