#!python

import csv
import requests
import numpy as np
import time
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

while True:
    api_key_file = open("api_key.txt", "r+")
    api_key = api_key_file.readline()

    api_lp_url = 'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/'

    playerNameList = ["Player Name"]
    playerLpList = ["Current LP"]

    counter = 0
    actualCounter = 0

    with open('playerListWithIds.csv', encoding="utf8", newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    print("Getting summoners' LPs.")

    for summoner, id in data[1:]:
        print(actualCounter)
        actualCounter = actualCounter + 1
        counter = counter + 1
        if (counter >= 95):
            counter = 0
            print("Reached rate limit of 100. Sleeping for 2 minutes")
            time.sleep(120)

        getLpUrl = api_lp_url + id + "?api_key=" + api_key
        resp = requests.get(getLpUrl)
        playerLpInfo = resp.json()
        if (playerLpInfo[0]['queueType'] == "RANKED_TFT"):
            if "leaguePoints" in playerLpInfo[0]:
                playerLp = playerLpInfo[0]['leaguePoints']
            else:
                playerLp = 0
                print(f'{summoner}\'s LP could not be found.')
        elif (playerLpInfo[1]['queueType'] == "RANKED_TFT"):
            if "leaguePoints" in playerLpInfo[1]:
                playerLp = playerLpInfo[1]['leaguePoints']
            else:
                playerLp = 0
                print(f'{summoner}\'s LP could not be found.')
        elif (playerLpInfo[2]['queueType'] == "RANKED_TFT"):
            if "leaguePoints" in playerLpInfo[2]:
                playerLp = playerLpInfo[2]['leaguePoints']
            else:
                playerLp = 0
                print(f'{summoner}\'s LP could not be found.')
        else:
            playerLp = 0
            print(f'{summoner}\'s LP could not be found.')

        playerNameList.append(summoner)
        playerLpList.append(playerLp)

    np.savetxt('playerListWithLP.csv', [p for p in zip(playerNameList, playerLpList)], delimiter=',', fmt='%s', encoding='utf-8')

    df = pd.read_csv("playerListWithLP.csv")
    sorted_df = df.sort_values(by=["Current LP"], ascending=False)
    sorted_df.to_csv('sorted_PlayerList_with_LP.csv', index=False)


    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('LP Tracker for TT1')

    with open('sorted_PlayerList_with_LP.csv', 'r', encoding='utf-8') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)

    spreadsheet2 = client.open('Updated Time')
    ws = spreadsheet2.get_worksheet(0)
    ws.update_cell(1, 1, datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    print("Restarting script!")