import threading
import datetime
import calendar
import time 
from Database import Database
import ferien
import socket
import schedule
from config import Check as C 
class Check(threading.Thread):

    def getoneDayinfuture(self):
        now=datetime.datetime.now()
        Year=now.strftime("%Y")
        if int(now.strftime("%d"))+1>=calendar.monthrange(int(now.strftime("%Y")),int(now.strftime("%m")))[1]:
            Month=str(int(now.strftime("%m"))+1)
            if int(now.strftime("%m"))+1>12:
                Year=str(int(now.strftime("%Y"))+1)
                Month="01"
            Day="01"
        else:
            Day=str(int(now.strftime("%d"))+1)
            Month=now.strftime("%m")
        if len(Day)==1:
            Day="0"+Day
        Date="{0}-{1}-{2}".format(Year,Month,Day)
        print(Date)

    def isschoolday(self):
        if ferien.current_vacation("NI")==None:
            return True
        return False
        
                
    def work(self):
        D=Database()
        D.cursor.execute('''show tables''')
        Tables=D.cursor.fetchall()
        if self.getoneDayinfuture() not in Tables and self.isschoolday():
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
                sock.connect((C.host,C.port))
                sock.sendall("POST (Iserv,Arvid)")#<-Setup reqired
    def run(self):
        schedule.every().day.at("15:00").do(self.work)
        while True:
            schedule.run_pending()
            time.sleep(30)
if __name__=="__main__":
    K=Check()
    K.start()