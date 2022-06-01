import json


fileNames = ["Wm_Parses.json", "WmTBC_Parses.json", "bene_Parses.json"]

uniqueChars = set()

expacParses = []

startTimes = [0]
endTimes = [0]

wmToBeneMap = {"Justin" : "Justinjr", "Abstinence" : "Abjection", "Barnabris" : "Barnabae",
               "Digie" : "Digitalz", "Jahmee" : "Jaamii", "Kang" : "Kangdude", "Kinastra" : "Kinestra",
               "Nashy" : "Nashborne", "Rayas" : "Rayashaman", "Zeion" : "Seion"}

classDistr = {}

for name in fileNames:

    print("-----------------------" + name)

    f = open(name)

    js = json.load(f)

    keys = list(js.keys())

    parses = {'dps' : {}, 'tanks' : {}, 'healers': {}}

    for i in range(1, int(max(keys)) + 1):

        for report in js[str(i)]['reportData']['reports']['data']:
            #try: 
                startTime = int(report['startTime'])
                endTime = int(report['endTime'])

                isDuplciateReport = False
                for timeStamp in startTimes:
                   if (abs(startTime - timeStamp) < 300000):
                       print("duplicate report found")
                       isDuplciateReport = True
                
                for endtimeStamp in endTimes:
                   if (abs(endTime - endtimeStamp) < 300000):
                       print("duplicate report found")
                       isDuplciateReport = True
                
                if (isDuplciateReport == True):
                    continue

                startTimes.append(startTime)
                endTimes.append(endTime)

                for role in parses.keys():
                    if (len(report['rankings']['data']) > 0):
                     for character in report['rankings']['data'][0]['roles'][role]['characters']:
                        user = character['name']
                        parse = character['bracketPercent']
                        uniqueChars.add(character['name'])
                        
                        if user in parses[role].keys():
                            parses[role][user].append(parse)
                        else:
                            parses[role][user] = [parse]
                            classDistr[user] = character['class']
            #except:
                continue
    
    expacParses.append(parses)

# merge wmTBC with beneTBC

duplicateNames = {}

for role in expacParses[1]:
        for char in expacParses[1][role]:
            if char in wmToBeneMap.keys():
                print("found mapped name from: " + char + " to " + wmToBeneMap[char] + " at role: " + role)
                if (wmToBeneMap[char] in expacParses[2]):
                    expacParses[2][role][wmToBeneMap[char]] = expacParses[1][role][char] + expacParses[2][role][wmToBeneMap[char]]
                duplicateNames[char] = role

# remove old parses from old name
for name in duplicateNames.keys():
    expacParses[1][duplicateNames[name]].pop(name)

# merge two TBC lists
expacParses[1].update(expacParses[2])

expacParses.remove(expacParses[2])

#calc averages and replace list of parses with avg
for expac in expacParses:           
    for role in expac:
        for char in expac[role]:
            sum = 0

            if not(isinstance(expac[role][char], list)):
                expac[role][char] = [expac[role][char]]

            for number in expac[role][char]:
                sum += number

            if (len(expac[role][char]) > 25):
                sum = sum / len(expac[role][char])
                expac[role][char] = sum
            else:
                expac[role][char] = 0

expacTops = []

#calc tops
for expac in expacParses:   
     tops = {'dps' : [], 'tanks' : [], 'healers': []}
     for role in expac.keys():
        for char in expac[role]:
            minTop = 10000000
            minIndex = -1
            for topEntry in tops[role]:
                if topEntry[1] < minTop:
                    minTop = topEntry[1]
                    minIndex = tops[role].index(topEntry)
            if expac[role][char] > minTop or len(tops[role]) < 3:
                maxName = char
                maxParse = expac[role][char]
                if len(tops[role]) >= 3:
                    tops[role].pop(minIndex)
                tops[role].append([maxName, maxParse])

     expacTops.append(tops)


print("Vanilla tops: ")
print(expacTops[0])

print("TBC tops: ")
print(expacTops[1])

print("Unique raiders: " + str(len(uniqueChars)))


classDistribution = {}

for Class in classDistr.values():
                        if Class in classDistribution.keys():
                            classDistribution[Class] += 1
                        else:
                            classDistribution[Class] = 1 

print(classDistribution)