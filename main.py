from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import date, datetime
from time import mktime
import base64
from requests import request
from pprint import pprint
import json
import pymssql
from datetime import datetime,timedelta

app_id = '1a05ff6ce5734d2aacac7e0969a53ade'
app_key = 'Gpt_U47acZpGT1HAojFgO1q6Hgw'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':

    keynum = int(input("請輸入搜尋的天數(最多10天) :)"))

    if(keynum > 10):
        print("錯誤")
    else:
        conn = pymssql.connect("127.0.0.1", "sa", "chi", "work")
        cursor = conn.cursor()
        
        a = Auth(app_id, app_key)
        
        station = ["0990","1000","1010","1020","1030","1035","1040","1043","1047","1050","1060","1070"]

        d1 = datetime.now()
        for i in range(0,keynum):    
            d3 = d1 + timedelta(days=i)

            for j in range(0,len(station)):
                for l in reversed(range(0,len(station))):
                    url = 'https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/' + station[j] + '/to/' + station[l] + '/' + d3.strftime('%Y-%m-%d') + '?%24top=10000&%24format=JSON'
                    response = request('get', url, headers= a.get_auth_header())
                    content = response.content.decode()  #重新編碼 預設空的為utf8
                    data = json.loads(content)
                    
                    for k in data:
                        item = list(k.values())
                        TrainDate = "('" + item[0] + "' ,"
                        TrainNO = "'" + item[1]["TrainNo"] + "' ,"
                        StationName = " '" + item[2]["StationName"]["Zh_tw"] + "' ,"
                        ArrivalTime = " '" + item[2]["ArrivalTime"] + "' ,"
                        StartSequence = " '" + str(item[2]['StopSequence']) + "' ,"

                        EndName = " '" + item[3]["StationName"]["Zh_tw"] + "' ,"
                        EndTime = " '" + item[3]["ArrivalTime"]+ "' ,"
                        StopSequence = " '" + str(item[3]["StopSequence"]) + "')"

                        query = "insert into Timetable (日期,車號,起站,起站時間,StartSequence,驛站,驛站時間,StopSequence) VALUES "
                        comment = query + TrainDate + TrainNO + StationName + ArrivalTime + StartSequence + EndName + EndTime + StopSequence
                        # print(comment)
                        cursor.execute(comment)
                        # 如果沒有指定autocommit屬性為True的話就需要呼叫commit()方法
                        conn.commit()