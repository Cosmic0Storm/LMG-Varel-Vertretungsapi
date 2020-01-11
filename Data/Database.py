import mysql.connector
from Data.Base import Data
from Data.config import Mysql
class Database:

    def __init__(self):
        self.sql=mysql.connector.connect(
            host=Mysql.host,
            user=Mysql.user,
            passwd=Mysql.paswd,
            database=Mysql.database
        )
        self.cursor=self.sql.cursor()

    def set(self,Data):
        if not isinstance(Data,Data.__class__):
            return
        self.cursor.execute("show tables")
        if (Data.Name,) not in self.cursor.fetchall():
            self.cursor.execute('''CREATE TABLE  if not exists`{0}` (   `Klasse` tinytext,   `Stunde` tinytext,   `Vertreter` tinytext,   `Fach` tinytext,   `Raum` tinytext,   `Entfallener_Lehrer` tinytext,   `Entfallenes_Fach` tinytext) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(Data.Name))
        for a in range(len(Data.Table)):
            self.cursor.execute("""UPDATE `{name}` SET `Vertreter`='{2}',`Fach`='{3}',`Raum`='{4}',`Entfallener_Lehrer`='{5}',`Entfallenes_Fach`='{6}' WHERE `Klasse`='{0}' AND `Stunde`='{1}'; """.format(*Data.Table[a],name=Data.Name))
            self.cursor.execute("""SELECT COUNT(1) FROM `{name}` WHERE `Klasse`='{0}' and `Stunde`='{1}'""".format(*Data.Table[a],name=Data.Name))
            if  self.cursor.fetchall()[0][0]==0:
                self.cursor.execute('''INSERT INTO `{name}` VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}');'''.format(*Data.Table[a],name=Data.Name))
        self.cursor.execute("select * from `{name}`".format(name=Data.Name))
        Table=self.cursor.fetchall()
        for c in range(len(Table)):
            if list(Table[c]) not in Data.Table:
                self.cursor.execute('''delete from `{name}` where `Klasse`='{0}' and `Fach`='{3}' and `Stunde`='{1}' '''.format(*Table[c],name=Data.Name))
        self.sql.commit()
    def get(self,json):
        if not json['Nutzer']['Erweitert']:
            self.cursor.execute("select * from `{name}` where `Klasse`='{Klasse}'".format(name=json['Date'],Klasse=json['Nutzer']['Klasse']))
            Klasse=self.cursor.fetchall()
            Res=[]
            for row in Klasse:
                if len(row[6])>2 and any(i.isdigit() for i in row[6]) and row[6] in json['Nutzer']['Kurse']:
                        Res.append(row)
                elif row[6] in ["LA","FR","SPA"] and row[6] in json['Nutzer']['Kurse']:
                    Res.append(row)
                elif  not any(i.isdigit() for i in row[6]) and row[6].isupper():
                    Res.append(row)
        else:
            self.cursor.execute('''select * from `{name}`'''.format(name=json['Date']))
            tupRes=self.cursor.fetchall()
            Res=[]
            for tup in tupRes:
                Res.append(list(tup))
        return Res

    def getTables(self):
        self.cursor.execute('show tables')
        return self.cursor.fetchall()
