import json 



with open('2021_12_23.json',encoding = 'utf8') as f:
    data = json.load(f)

    for i in data:
        item = list(i.values())
        TrainNO = " '" + item[1]["TrainNo"] + "' ,"
        StationName = " '" + item[2]["StationName"]["Zh_tw"] + "' ,"
        ArrivalTime = " '" + item[2]["ArrivalTime"] + "' ,"
        EndName = " '" + item[3]["StationName"]["Zh_tw"] + "' ,"
        EndTime = " '" + item[3]["ArrivalTime"]+ "' ,"

        print(TrainNO + StationName + ArrivalTime + EndName + EndTime)