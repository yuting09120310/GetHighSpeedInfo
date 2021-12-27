import json 
import requests


with open('2021_12_23.json',encoding = 'utf8') as f:
    data = json.load(f)
    print(type(data))

    for i in data:
        item = list(i.values())
        # TrainNO = " '" + item[1]["TrainNo"] + "' ,"
        # StationName = " '" + item[2]["StationName"]["Zh_tw"] + "' ,"
        # ArrivalTime = " '" + item[2]["ArrivalTime"] + "' ,"
        # EndName = " '" + item[3]["StationName"]["Zh_tw"] + "' ,"
        # EndTime = " '" + item[3]["ArrivalTime"]+ "'"
        EndTime = item[2]['StopSequence']
        # print(TrainNO + StationName + ArrivalTime + EndName + EndTime)

        print(EndTime)