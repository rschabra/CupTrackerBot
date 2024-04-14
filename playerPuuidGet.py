#!python

import csv
import requests
import numpy as np
import time

api_key_file = open("api_key.txt", "r+")
api_key = api_key_file.readline()

get_puid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

playerNameList = ["Player Name"]
playerLpList = ["Player Puuid"]

counter = 0
actualCounter = 0

with open('playerlist.csv', encoding="utf8", newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

print("Getting summoners' puuids.")
for summoner in data:
    print(actualCounter)
    actualCounter = actualCounter + 1
    counter = counter + 1
    if (counter >= 98):
        counter = 0
        time.sleep(120)
        print("Reached rate limit of 100. Sleeping for 2 minutes")


    head, sep, tail = summoner[0].partition('#')
    head.replace(" ", "%20")
    getPuuid = get_puid_url + head + "/" + tail + "?api_key=" + api_key

    respPuuid = requests.get(getPuuid)

    playerByRiotID = respPuuid.json()

    playerPuuid = playerByRiotID["puuid"]

    playerNameList.append(summoner[0])
    playerLpList.append(playerPuuid)

np.savetxt('playerListWithPuuid.csv', [p for p in zip(playerNameList, playerLpList)], delimiter=',', fmt='%s', encoding='utf-8')
