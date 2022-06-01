from os import walk
import json

fileNames = ["playerDeaths_Wm.json", "playerDeaths_WmTBC.json", "playerDeaths_Bene.json",]

wmToBeneMap = {"Justin" : "Justinjr", "Abstinence" : "Abjection", "Barnabris" : "Barnabae",
               "Digie" : "Digitalz", "Jahmee" : "Jaamii", "Kang" : "Kangdude", "Kinastra" : "Kinestra",
               "Nashy" : "Nashborne", "Rayas" : "Rayashaman", "Zeion" : "Seion"}


expacDeaths = []

for name in fileNames:

    print("-----------------------" + name)

    totalTime = 0
    f = open(name)

    js = json.load(f)

    keys = list(js.keys())
    
    wipeCounter = {}

    if name == "playerDeaths_Wm.json":
        direct = "playerDeathsWm"
    if name == "playerDeaths_Bene.json":
        direct = "playerDeathsBene"
    if name == "playerDeaths_WmTBC.json":
        direct = "playerDeathsWmTBC"    

    filenamesJSON = next(walk(direct), (None, None, []))[2]  # [] if no file

    playerDeaths = {}

    for i in range(1, int(max(keys)) + 1):

        for file in filenamesJSON:
            f = open(direct+ "/" + file)

            js = json.load(f)
  
            for player in js:
                if player in playerDeaths.keys():
                  playerDeaths[player] += js[player]
                else:
                  playerDeaths[player] = js[player]
        
    expacDeaths.append(playerDeaths)

duplicateNames = []

for char in expacDeaths[1]:
    if char in wmToBeneMap.keys():
        print("found mapped name from: " + char + " to " + wmToBeneMap[char])
        if (wmToBeneMap[char] in expacDeaths[2]):
            expacDeaths[2][wmToBeneMap[char]] = expacDeaths[1][char] + expacDeaths[2][wmToBeneMap[char]]
            duplicateNames.append(char)

# remove old parses from old name
for name in duplicateNames:
    expacDeaths[1].pop(name)

# merge two TBC lists
expacDeaths[1].update(expacDeaths[2])

# delete one of the lists
expacDeaths.remove(expacDeaths[2])

print(len(expacDeaths))

expacTops = []

for expac in expacDeaths:
    top = []
    
    maxName = ""
    maxDeaths = 0

    for k in expac.keys():
        minTop = 10000000
        minIndex = -1
        for topEntry in top:
            if topEntry[1] < minTop:
                minTop = topEntry[1]
                minIndex = top.index(topEntry)
        if expac[k] > minTop or len(top) < 3:
            maxName = k
            maxDeaths = expac[k]
            if len(top) >= 3:
                top.pop(minIndex)
            top.append([maxName, maxDeaths])
    
    expacTops.append(top)
    
    

    
print("\n")
    
print(expacTops)

