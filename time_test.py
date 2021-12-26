import datetime

d1 = datetime.datetime.now()
for i in range(1,7):
    d3 = d1 + datetime.timedelta(days=i)
    data ='https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/0990/to/1010/' + d3.strftime('%Y-%m-%d') + '?%24top=10000&%24format=JSON'
    print (data)