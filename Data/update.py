import threading
from bs4 import BeautifulSoup
import requests
import schedule
import time
from Base import Data
from Database import Database
from config import Iserv
class Update_Thread(threading.Thread):
    URls={"login":"https://lmg-varel.eu/iserv/login_check",
          "morgen":"https://lmg-varel.eu/iserv/infodisplay/file/205/plan/0/schuelermorgeninternet/subst_001.htm",
          "heute":"https://lmg-varel.eu/iserv/infodisplay/file/205/plan/0/schuelerheuteinternet/subst_001.htm"}
    def __init__(self,Type):
        print(self.URls[Type])
        threading.Thread.__init__(self)
        self.url=self.URls[Type]
        self.akttime= 5 if Type=="morgen" else 30
        self.Data=Data("dd.MM.YYYY HH:MM",[[]],"dd.MM.YYYY dofWw")
        self.DB=Database()
    def getData(self):
        Params = {'_username':Iserv.user,'_password':Iserv.paswd}#Needs Valid User and Password for Iserv-Lmg
        with requests.Session() as s:
            r = s.post(self.URls["login"], data=Params)
            data = s.post(self.url)
            s.close()
        soup = BeautifulSoup(data.text, 'html.parser')
        Table = []
        Res_List = []
        newsoup = soup.find('table', {'class': 'mon_list'})
        for tr in newsoup.find_all('tr'):
            row=[]
            for td in tr.find_all('td'):
                if td.text=="\xa0":
                    continue
                elif td.text=="x":
                    continue
                else:
                    row.append(td.text)
            if len(row)>0:
                Table.append(row)
        Standsoup=soup.find("p")
        Stand=Standsoup.text[Standsoup.text.find("Stand")+7:]
        print(Stand)
        Namesoup=soup.find("div",{"class":"mon_title"})
        print(Namesoup.text) 
        return Data(Stand,Table,Namesoup.text)
    def work(self):
        try:
            print("Woke up")
            nData=self.getData()
            print(self.Data==nData)
            if self.Data!=nData:
                print("Data anders")
                print(nData.Table)
                self.DB.set(nData)
                self.Data=nData 
        except requests.exceptions.ConnectionError as errc:
            print('ConnectionError')
            print(errc)
             
        except requests.exceptions.ReadTimeout as errc:
            print('ReadTimeout')
            print(errc)

    def run(self):
        self.work()
        schedule.every(5).minutes.do(self.work)
        schedule.every().day.at("00:00").do(self.Data.clear)
        while True:
            schedule.run_pending()
            time.sleep(10)
    
if __name__=="__main__":
    Heute=Update_Thread("heute").start()
    Morgen=Update_Thread("morgen").start()
    #C=Check()
    #C.start()
    
    