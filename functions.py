from datetime import datetime, timedelta

def getDate(str,offset=0):
    if str=="heute":
        m=datetime.now()-timedelta(days=offset)
        return m.strftime("%Y-%m-%d")
    elif str=="morgen":
        m=datetime.now()+timedelta(days=1)
        return m.strftime("%Y-%m-%d")


if __name__ == '__main__':
    print(getDate("morgen"))