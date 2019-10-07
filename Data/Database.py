import mysql.connector
from Base import Data
class Database:

    def __init__(self):
        self.sql=mysql.connector.connect(
            host="localhost",
            user="Iservtest",
            passwd="a-sdgd-adadolä",
            database="Iservtest"
        )
        self.cursor=self.sql.cursor()

    def set(self,Data):
        print(Data.Name)
        if not isinstance(Data,Data.__class__):
            print("IDiot")
            return
        self.cursor.execute("show tables")
        if Data.Name not in self.cursor.fetchall():
            self.cursor.execute('''CREATE TABLE  if not exists`{0}` (   `Klasse` tinytext,   `Stunde` tinytext,   `Vertreter` tinytext,   `Fach` tinytext,   `Raum` tinytext,   `Entfallener_Lehrer` tinytext,   `Entfallenes_Fach` tinytext) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(Data.Name))
        for a in range(len(Data.Table)):
            self.cursor.execute("""UPDATE `{name}` SET `Vertreter`='{2}',`Fach`='{3}',`Raum`='{4}',`Entfallener_Lehrer`='{5}',`Entfallenes_Fach`='{6}' WHERE `Klasse`='{0}' AND `Stunde`='{1}'; """.format(*Data.Table[a],name=Data.Name))
            self.cursor.execute("""SELECT COUNT(1) FROM `{name}` WHERE `Klasse`='{0}' and `Stunde`='{1}'""".format(*Data.Table[a],name=Data.Name))
            if  self.cursor.fetchall()[0][0]==0:
                self.cursor.execute('''INSERT INTO `{name}` VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}');'''.format(*Data.Table[a],name=Data.Name))
        self.cursor.execute("select * from `{name}`".format(name=Data.Name))
        Table=self.cursor.fetchall()
        print(Data.Table)
        for c in range(len(Table)):
            if list(Table[c]) not in Data.Table:
                print(list(Table[c]))
                self.cursor.execute('''delete from `{name}` where `Klasse`='{0}' and `Fach`='{3}' and `Stunde`='{1}' '''.format(*Table[c],name=Data.Name))
        self.sql.commit()
    def get(self,Req):
        print((Req.Day,Req.Klasse))
        if not Req.All:
            self.cursor.execute("select * from `{name}` where `Klasse`='{Klasse}'".format(name=Req.Day,Klasse=Req.Klasse))
            Klasse=self.cursor.fetchall()
            Res=[]
            for row in Klasse:
                print(row)
                print(not any(i.isdigit() for i in row[3]) and row[3].isupper())
                if len(row[3])>2 and any(i.isdigit() for i in row[3]) and row[3] in Req.Kurse:
                        Res.append(row)
                elif row[3] in ["LA","FR","SPA"] and row[3] in Req.Kurse:
                    Res.append(row)
                elif int(Req.Klasse.strip(Req.Klasse[-1]))>9 and "ge" in row[3]: #<- add Special Cases
                    Res.append(row)
                elif  not any(i.isdigit() for i in row[3]) and row[3].isupper():
                    Res.append(row)
        else:
            self.cursor.execute('''select * from `{name}`'''.format(name=Req.Day))
            tupRes=self.cursor.fetchall()
            Res=[]
            for tup in tupRes:
                Res.append(list(tup))
            print(Res)
        print(Res)
        return Res
    def log(self,Info):
        pass
