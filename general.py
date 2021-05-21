import datetime
def getDate(d):
    curr = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
    print(curr)

getDate(1)