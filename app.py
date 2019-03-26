#!/usr/bin/env python
import sqlite3 as sql
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

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
    #peech_text=[]
    con = sql.connect("database.db")
    cur=con.cursor()
    if con:
        print ("Connected database successfully")
    else:
        print("connect failed")
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
    speech_text=[]
    test_code=[]
    #print("this is mine"+ req.get("result").get("action"))
    result = req.get("result")
    print(result)
    parameters = result.get("parameters")
    skillset = parameters.get("skills-list")
#     cur.prepare('select * from mytable where skill = :skills-list')
#     cur.execute(None, {'skill': skillset})
    cur.execute('select * from mytable where skill = ?',['skillset'])
    rows = cur.fetchall()
    for row in rows:
        speech_text.append(row[0])
    
#     with sql.connect("database.db") as con:
#         cur = con.cursor()
#         con.row_factory = sql.Row
#         cur = con.cursor()
#         cur.execute("select * from mytable where city= ?",[zone])
#         rows = cur.fetchall()
#         for row in rows:
#             speech_text.append(row[0])
    con.close()
    speechtext=list(set(speech_text))
    print(speechtext)
    speech="The candidates for skill  "+skillset+ "  are :  " + "{}.".format(','.join(speechtext))        
            
        #print(row[0],row[1],row[2],row[3])
    #print(rows)

    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": "It's done",
        #"data": {},
        # "contextOut": [],
        "source": "skills database"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    #
    print ("Starting app on port %d" % port)
    #app.run()
    app.run(debug=True, port=port, host='0.0.0.0')
