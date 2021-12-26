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

        d1 = datetime.now()
        for i in range(1,keynum):
            d3 = d1 + timedelta(days=i)
            url = 'https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/0990/to/1010/' + d3.strftime('%Y-%m-%d') + '?%24top=10000&%24format=JSON'
            response = request('get', url, headers= a.get_auth_header())
            content = response.content.decode()  #重新編碼 預設空的為utf8
            data = json.loads(content)
            
            for i in data:
                item = list(i.values())
                TrainDate = "('" + item[0] + "' ,"
                TrainNO = "'" + item[1]["TrainNo"] + "' ,"
                StationName = " '" + item[2]["StationName"]["Zh_tw"] + "' ,"
                ArrivalTime = " '" + item[2]["ArrivalTime"] + "' ,"
                EndName = " '" + item[3]["StationName"]["Zh_tw"] + "' ,"
                EndTime = " '" + item[3]["ArrivalTime"]+ "')"

                query = "insert into Timetable (日期,車號,起站,起站時間,驛站,驛站時間) VALUES "
                comment = query + TrainDate + TrainNO + StationName + ArrivalTime + EndName + EndTime
                # print(comment)
                cursor.execute(comment)
                # 如果沒有指定autocommit屬性為True的話就需要呼叫commit()方法
                conn.commit()