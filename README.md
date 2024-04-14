# TFT Cup Snapshot Tracker


## Install

Confirm python is installed on your PC. On Windows this can be done through the Windows Store.

Run `pip install -r requirements.txt`.

## Setup

Open `api_key.txt` and paste your Riot Developer api_key.

Your riot development API key is available here: https://developer.riotgames.com. Please note this key expires every 24 hours.

Paste riot ids of all participants in the playerlist.csv file. This can be done using the Riot website and copying the ids into an excel sheet. Once they are in the excel sheet the other columns can be removed and this sheet can be downloaded as a csv file.

## Run

Open Git Bash, or anywhere you are able to run python via the command line.

- If first run (playerLists are not populated), please run the following command **`./firstRun.sh`**
- If playerLists have been previously populated for this cup, please run the following command **`./refreshLpList.sh`**

## Refreshing the LP List

Once the run has completed, a sorted_PlayerList_with_LP.csv file will have been generated. This file can be opened in Google Sheets or Excel and formatted appropriately.



