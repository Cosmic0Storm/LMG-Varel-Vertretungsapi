import mysql.connector
from Base import Data
from config import Mysql
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
        for a in range(len(Data.Table)):
            self.cursor.execute("""UPDATE `Vertretungsplan` SET `Date`='{date}',`Vertreter`='{2}',`Fach`='{3}',`Raum`='{4}',`Entfallener_Lehrer`='{5}',`Entfallenes_Fach`='{6}' WHERE `Klasse`='{0}' AND `Stunde`='{1}'; """.format(*Data.Table[a],date=Data.Name))
            self.cursor.execute("""SELECT COUNT(1) FROM `Vertretungsplan` WHERE `Klasse`='{0}' and `Stunde`='{1}' and `Date`='{date}'""".format(*Data.Table[a],date=Data.Name))
            if  self.cursor.fetchall()[0][0]==0:
                self.cursor.execute('''INSERT INTO `Vertretungsplan` VALUES('{date}','{0}','{1}','{2}','{3}','{4}','{5}','{6}');'''.format(*Data.Table[a],date=Data.Name))
        self.cursor.execute("select * from `Vertretungsplan`")
        Table=self.cursor.fetchall()
        for c in range(len(Table)):
            if list(Table[c]) not in Data.Table:
                self.cursor.execute('''delete from `Vertretungsplan` where `Klasse`='{0}' and `Fach`='{3}' and `Stunde`='{1}' and `Date`='{date}'  '''.format(*Table[c],date=Data.Name))
        self.sql.commit()

    def setup(self):
        self.cursor.execute('''CREATE TABLE  if not exists`Vertretungsplan` (   `Date` tinytext,`Klasse` tinytext,   `Stunde` tinytext,   `Vertreter` tinytext,   `Fach` tinytext,   `Raum` tinytext,   `Entfallener_Lehrer` tinytext,   `Entfallenes_Fach` tinytext) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
