import json


fileNames = ["LootHistory_Timestamp_Desc_Vanilla.json", "LootHistory_Timestamp_Desc.json"]

uniqueChars = set()

expacParses = []

wmToBeneMap = {"Justin" : "Justinjr", "Abstinence" : "Abjection", "Barnabris" : "Barnabae",
               "Digie" : "Digitalz", "Jahmee" : "Jaamii", "Kang" : "Kangdude", "Kinastra" : "Kinestra",
               "Nashy" : "Nashborne", "Rayas" : "Rayashaman", "Zeion" : "Seion"}

lowestDKP = 9999999
lowestDKPTrans = {}

DKPTotal = 0
DKPTransactions = 0

numTrans = {}

for name in fileNames:

    print("-------------------------" + name)

    f = open(name)

    js = json.load(f)

    for transaction in js:
        user = transaction['Recipient']

        if user == "N/A":
            continue

        DKPTotal += transaction['DKPBefore'] - transaction['DKPAfter']
        DKPTransactions += 1
        if user in numTrans.keys():
            numTrans[user] += 1
        else:
            numTrans[user] = 1

        if transaction['DKPAfter'] < lowestDKP:
            lowestDKP = transaction['DKPAfter']
            lowestDKPTrans = transaction

    print("--------------------end")


duplicateNames = []

#map user names to transfer names
for char in numTrans:
    if (char in wmToBeneMap.keys()):
        print("found mapped name from: " + char + " to " + wmToBeneMap[char])
        numTrans[wmToBeneMap[char]] += numTrans[char]
        duplicateNames.append(char)

for char in duplicateNames:
    numTrans.pop(char)



# find top DKP users
top = []

for user in numTrans:
    
    if user == "N/A":
        continue

    maxName = ""
    maxDeaths = 0
    
    minTop = 10000000
    minIndex = -1
    for topEntry in top:
        if topEntry[1] < minTop:
            minTop = topEntry[1]
            minIndex = top.index(topEntry)

    if numTrans[user] > minTop or len(top) < 3:
        maxName = user
        maxDeaths = numTrans[user]
        if len(top) >= 3:
            top.pop(minIndex)
        top.append([maxName, maxDeaths])

print("Lowest char: " + lowestDKPTrans['Recipient'])
print("Lowest DKP: " + str(lowestDKP))

print(top)

print("DKPTransactions: " + str(DKPTransactions))
print("DKP Total: " + str(DKPTotal))

