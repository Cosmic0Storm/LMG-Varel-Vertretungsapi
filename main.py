from flask import Flask
from flask_restplus import Api, Resource, fields
from Data.database import Database
from functions import getDate
app=Flask(__name__)
api=Api(app)

D=Database()
nutzer=api.model('Nutzer',{'Klasse':fields.String('Klasse des Nutzers'),'Kurse':fields.List(fields.String,description=u'Kurse des Nutzers'),'Erweitert':fields.Boolean(description='Ob alles angezeigt werden soll')})
req=api.model('Request',{'Date':fields.String('Datum YYYY-MM-dd or heute or  morgen'),'Nutzer':fields.Nested(nutzer)})
@api.route('/Vertretung')
class Vertretung(Resource):

    def get(self):
        return {'hey':'there'}

    @api.expect(req)
    def post(self):
        
        if api.payload['Date']=='heute':
            Date=getDate(api.payload['Date'])
            a=1
            while (Date,) not in D.getTables():
                Date=getDate(api.payload['Date'],offset=a)
                a+=1
            api.payload['Date']=Date

        elif api.payload['Date']=='morgen':
            api.payload['Date']=getDate(api.payload['Date'])
        Res=D.get(api.payload)
        print(Res)

        return {'Vertretung':Res}
                    
    

if __name__=='__main__':
    app.run(debug=True)