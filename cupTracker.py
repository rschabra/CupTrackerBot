import csv
import requests
import numpy as np
import time

api_key = "RGAPI-6de8acb3-5d7d-43ed-b545-3877515852ac"

get_puid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

api_id_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/'
api_lp_url = 'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/'

playerNameList = ["Player Name"]
playerLpList = ["Current LP"]

counter = 0
actualCounter = 0

with open('playerlist.csv', encoding="utf8", newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

for summoner in data:
    print(actualCounter)
    actualCounter = actualCounter + 1
    counter = counter + 1
    if (counter >= 48):
        counter = 0
        time.sleep(120)
        print("Reached rate limit of 100. Sleeping for 2 minutes")


    head, sep, tail = summoner[0].partition('#')
    head.replace(" ", "%20")
    getPuuid = get_puid_url + head + "/" + tail + "?api_key=" + api_key

    respPuuid = requests.get(getPuuid)

    playerByRiotID = respPuuid.json()

    playerPuuid = playerByRiotID["puuid"]

    getIdUrl = api_id_url + playerPuuid + "?api_key=" + api_key
    resp = requests.get(getIdUrl)
    playerInfo = resp.json()
    encryptedSummonerId = playerInfo['id']

    getLpUrl = api_lp_url + encryptedSummonerId + "?api_key=" + api_key
    respTwo = requests.get(getLpUrl)
    playerLpInfo = respTwo.json()
    playerLp = playerLpInfo[0]['leaguePoints']

    playerNameList.append(summoner[0])
    playerLpList.append(playerLp)

np.savetxt('playerListWithLP.csv', [p for p in zip(playerNameList, playerLpList)], delimiter=',', fmt='%s')