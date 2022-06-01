
accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NjNhYmZhOC1lMjkwLTQwNTYtYTlkYy0xMzY3YzBlNjlhNzUiLCJqdGkiOiJhZWIzZjdmMDY2NDY3YzU3N2NmMjRkMjAyODAxM2ZlYjE3NTFiMjU1NWUwMjU4ZmQ1NWY0ZjQ1ZGI1YTRiMzUzNGM0MzdiMGJhZGIxYTlhNCIsImlhdCI6MTY1MTc5MDc2My4zOTU5NTMsIm5iZiI6MTY1MTc5MDc2My4zOTU5NTYsImV4cCI6MTY2MjE1ODc2My4zODc0MjEsInN1YiI6IiIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.CwRauBHESG6ItLJtXSBPLYOuH4vkvBgRApqrPu8lfmNEkivsk3N9MzmgFAXSdo59YLpW6JsX8WKxNMhP6CfYB94VlTVbRJO14rZnlQolpswstKiAgzHbV3ouZLLfLfgYpwIBwO1ids2tsFv9sXji1pc7aCvL70yGC_Q2nux2B3CTVY83SJXJM84dhZYKTLIQVQIKMbSTjt3Wfm1j348-nnV3KpU7asv-VGOWi0px2mjuqFgZodW91I8E5ykiSkIE_cgMfGX6wf7FY-UT6DC28gj1Jw8p7gW_KuZGPoXRyIx3bKNWnzQvOS4Y95MmTML9u2xhbuSW2dK_GBzTl7PaQdUNc2kWyvC1XlDFVE4hd1bDNscSBxRq-aa6J4OxzFSFpGZcp5QE9qnwIFC4Ug1CBVsy4a4BX1iSonuXbQpC7HGyTisJeDc-izLINs9zmJ1ze_wj_GsYM9ncBy5gxK9yruJsG9kSQPyV9gJv8k2Q1l1OAMSjmVsse0RyKUwQSCoplPhGd9_kX7mXhAG84DxJyLVNHo6FPOK_mIA_mNDzkUwD4j8f-PYLc6Myqy_OvvjW34EcQdf2WteRZLBbe1F3Z_TH6hc9-cweK7v-4ehrwUl9HmvMPywsApeXRUFyZA8hPeWa9Sn1w-6bZX-M9wNqGDcYIThjC7wuj3VArDAeqZA"

import requests
import time
from datetime import datetime
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
apiUrl = 'https://classic.warcraftlogs.com/api/v2'
bearer = "Bearer " + accessToken
headers = {"Authorization": bearer}

def fetchGraphQL(query):
    #if data.get(query):
     #   return data.get(query).get('data')
    try:
        response = requests.post(apiUrl, json={'query': query}, headers=headers).json()
        #print(response)
        if not response or response.get('errors'):
            return {}
        else:
            return response.get('data')
    except Exception as e:
        print(e)
        print('Sleeping', datetime.now())
        time.sleep(60)
        fetchGraphQL(query)

def getPages(guildID, time):
    query = f'''
    {{
        reportData {{
            reports(guildID: {guildID}, startTime: {time[0]}, endTime: {time[1]}) {{
                last_page
            }}
        }}
    }}
    '''
    data = fetchGraphQL(query)

    return data['reportData']['reports']['last_page']

def getWipes(guildID, filename, time) -> dict:

    pages = getPages(guildID, time)
    data = {}

    for i in range(1,pages + 1):
        query = f'''
    {{
        reportData {{
            reports(guildID: {guildID}, startTime: {time[0]}, endTime: {time[1]}, page: {i}) {{
                data {{
                    startTime
                    fights(killType: Wipes){{
                        encounterID
                        endTime
                    }}
                }}
            }}
        }}
    }}
    '''
        data[i] = fetchGraphQL(query)

    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

def getRaidTime(guildID, filename, time) -> dict:

    pages = getPages(guildID, time)
    data = {}

    for i in range(1,pages + 1):
        query = f'''
    {{
        reportData {{
            reports(guildID: {guildID}, startTime: {time[0]}, endTime: {time[1]}, page: {i}) {{
                data {{
                    startTime
                    endTime
                }}
            }}
        }}
    }}
    '''
        data[i] = fetchGraphQL(query)

    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

def getPlayerDeaths(guildID, filename, time):
    pages = getPages(guildID, time)
    data = {}

    for i in range(1,pages + 1):
        query = f'''
    {{
        reportData {{
            reports(guildID: {guildID}, startTime: {time[0]}, endTime: {time[1]}, page: {i}) {{
                data {{
                    code
                    startTime
                    events(dataType: Deaths, startTime:0, endTime:999999){{
                        data
                    }}
                }}
            }}
        }}
    }}
    '''
        data[i] = fetchGraphQL(query)

    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

def getPlayerDeathCount(guildID, filename, dir):
    f = open(filename)
    js = json.load(f)

    actors = {}

    for report in js['1']['reportData']['reports']['data']:    
        query = f'''
    {{
        reportData {{
            report(code: "{str(report['code'])}") {{
                masterData {{
                    actors{{
                        name
                        id
                    }}
                }}
            }}
        }}
    }}
    '''
        masterData = fetchGraphQL(query)

        playerIDs = {}

        for actor in masterData['reportData']['report']['masterData']['actors']:
            playerIDs[actor['id']] = actor['name']

        playerDeaths = {}
        
        for death in report['events']['data']:
            playerID = death['targetID']

            if (not("feign" in death.keys())):
             if playerIDs[playerID] in playerDeaths.keys():
                playerDeaths[playerIDs[playerID]] += 1
             else:
                playerDeaths[playerIDs[playerID]] = 1
    
        file = open(dir + "/" + report['code'] + ".json", 'w')
        file.write(json.dumps(playerDeaths))
        file.close()

def getParses(guildID, filename, time):
    pages = getPages(guildID, time)
    data = {}

    for i in range(1,pages + 1):
        query = f'''
    {{
        reportData {{
            reports(guildID: {guildID}, startTime: {time[0]}, endTime: {time[1]}, page: {i}) {{
                data {{
                    startTime
                    endTime
                    rankings
                }}
            }}
        }}
    }}
    '''
        data[i] = fetchGraphQL(query)

    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

def getKills(guildID, filename, time):
    pages = getPages(guildID, time)
    data = {}

    for i in range(1,pages + 1):
        query = f'''
    {{
        reportData {{
            reports(guildID: {guildID}, startTime: {time[0]}, endTime: {time[1]}, page: {i}) {{
                data {{
                    startTime
                    fights(killType: Kills){{
                        encounterID
                        endTime
                    }}
                }}
            }}
        }}
    }}
    '''
        data[i] = fetchGraphQL(query)

    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

#bene 641343
#whitemane 478993

#TBC - 1622271531000

### BENE
timeframe = [float(0), float(1653806423843)]
#getKills(641343, "bene_Kills.json", timeframe)
#getWipes(641343, "wipes_Bene.json", timeframe)
#getPlayerDeaths(641343, "playerDeaths_Bene.json", timeframe)
#getPlayerDeathCount(641343, "playerDeaths_Bene.json", "playerDeathsBene")
#getParses(641343, "bene_Parses.json", timeframe)
#getRaidTime(641343, "bene_raidTime.json", timeframe)

### Whitemane tbc
timeframe = [float(1622271531000), float(1653806423843)]
#getKills(478993, "wmTBC_Kills.json", timeframe)
#getWipes(478993, "wipes_WmTBC.json", timeframe)
#getPlayerDeaths(478993, "playerDeaths_WmTBC.json", timeframe)
#getPlayerDeathCount(478993, "playerDeaths_WmTBC.json", "playerDeathsWmTBC")
#getParses(478993, "WmTBC_Parses.json", timeframe)
#getRaidTime(478993, "WmTBC_raidTime.json", timeframe)

### Whitemane vanilla
#timeframe = [float(0), float(1622271531000)]
#getKills(478993, "wm_Kills.json", timeframe)
#getWipes(478993, "wipes_Wm.json", timeframe)
#getPlayerDeaths(478993, "playerDeaths_Wm.json", timeframe)
#getPlayerDeathCount(478993, "playerDeaths_Wm.json", "playerDeathsWm")
#getParses(478993, "Wm_Parses.json", timeframe)
#getRaidTime(478993, "Wm_raidTime.json", timeframe)