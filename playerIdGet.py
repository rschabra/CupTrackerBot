#!python

import csv
import requests
import numpy as np
import time

api_key_file = open("api_key.txt", "r+")
api_key = api_key_file.readline()

api_id_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/'

playerNameList = ["Player Name"]
playerIdList = ["Player Id"]

counter = 0
actualCounter = 0

with open('playerListWithPuuid.csv', encoding="utf8", newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

print("Getting summoners' encrypted IDs.")
for summoner, pid in data[1:]:
    print(actualCounter)
    actualCounter = actualCounter + 1
    counter = counter + 1
    if (counter >= 95):
        counter = 0
        time.sleep(120)
        print("Reached rate limit of 100. Sleeping for 2 minutes")

    getIdUrl = api_id_url + pid + "?api_key=" + api_key
    resp = requests.get(getIdUrl)
    playerInfo = resp.json()
    encryptedSummonerId = playerInfo['id']

    playerNameList.append(summoner)
    playerIdList.append(encryptedSummonerId)

np.savetxt('playerListWithIds.csv', [p for p in zip(playerNameList, playerIdList)], delimiter=',', fmt='%s', encoding='utf-8')
