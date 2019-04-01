#!/usr/bin/env python
import sqlite3 as sql
import urllib
import json
import os


from flask import Flask
from flask import request
from flask import make_response
from flask_mail import Mail, Message

# Flask app should start in global layout
app = Flask(__name__)
@app.route('/insert')
def insert_data():
    with sql.connect("database.db") as con:
        con.execute('CREATE TABLE IF NOT EXISTS mytable (id INTEGER,name TEXT, skill TEXT,UNIQUE(id)) ')
        cur = con.cursor()
        cur.execute("INSERT INTO mytable (id,name,skill) VALUES (?,?,?)",(1,"user1","python"))
        cur.execute("INSERT INTO mytable (id,name,skill) VALUES (?,?,?)",(2,"user2","python"))
        cur.execute("INSERT INTO mytable (id,name,skill) VALUES (?,?,?)",(3,"user3","html"))
        cur.execute("INSERT INTO mytable (id,name,skill) VALUES (?,?,?)",(4,"user4","java"))
        cur.execute("INSERT INTO mytable (id,name,skill) VALUES (?,?,?)",(5,"user5","jsf"))
        con.commit()
        print("Record successfully added")
        con.close()
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/webhook', methods=['POST'])
def webhook():
#     result=cur.execute("select * from mytable")
#     rows=result.fetchall()
#     for row in rows:
#         speech_text.append(row[1])
#     speechtext=list(set(speech_text))
#     speech="The candidates are :  " + "{}.".format(','.join(speechtext))
#     print(speech)
#     op={'speech':speech}
#     res=json.dumps(op,indent=4)
#     r=make_response(res)
#     r.headers['Content-Type'] = 'application/json'
#     return r
    #return result

    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    con = sql.connect("database.db")
    cur=con.cursor()
    speech_text=[]
    test_code=[]
    #print("this is mine"+ req.get("result").get("action"))
    result = req.get("result")
    print(result)
    skillset = result.get("resolvedQuery")
    #skillset = parameters.get("skills-list")
    print(skillset)
    if skillset=='yes':
        mail_settings = {
            "MAIL_SERVER": 'smtp.gmail.com',
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": 'proprietrymail@gmail.com',
            "MAIL_PASSWORD": 'gmailrajkamal8979'
        }
        app.config.update(mail_settings)
        mail = Mail(app)
        with app.app_context():
            msg = Message(subject="WELCOME DEAR",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["rajkamal8979@gmail.com"], # replace with your email for testing
                      body="Here I have prepared a special iternary for you! Follow the below attached email: https://drive.google.com/open?id=1ACkjHzQLlW7ie4gxIVXmBRCHeKLh5wj-G5EzTBOt4x4")
            mail.send(msg)
        return {
            "speech": 'Congratulations. Enjoy your special Day'
        }
    else:
        return {
            "speech": 'This is a surprise. So just say yes, It is mandatory.'
        }
        
    # print("Executing Query")
    # cur.execute("select * from mytable where skill = ?",(skillset,))
    # print(cur)
    # rows = cur.fetchall()
    # for row in rows:
    #     speech_text.append(row[1])
    #
    # print(speech_text)
    # speechtext=list(set(speech_text))
    # print(speechtext)
    # speech="The candidates for skill  "+skillset+ "  are :  " + "{}.".format(','.join(speechtext))
    #
    # print("Response:")
    # print(speech)
    # con.close()

   



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    #
    print ("Starting app on port %d" % port)
    #app.run()
    app.run(debug=True, port=port, host='0.0.0.0')
