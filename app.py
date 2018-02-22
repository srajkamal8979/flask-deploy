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
con = sql.connect('database.db')
print ("Opened database successfully")
con.execute('CREATE TABLE IF NOT EXISTS mytable (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print ("Table created successfully")
with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO mytable (name,addr,city,pin) VALUES (?,?,?,?)",("Raj","inngr","python",102))
    cur.execute("INSERT INTO mytable (name,addr,city,pin) VALUES (?,?,?,?)",("mona","inngr","java",103))
    cur.execute("INSERT INTO mytable (name,addr,city,pin) VALUES (?,?,?,?)",("mona","inngr","jsf",104))
    con.commit()
    print("Record successfully added")
con.close()

@app.route('/webhook', methods=['POST'])
def webhook():
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
    
    
    print("this is mine"+ req.get("result").get("action"))
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    
    with sql.connect("database.db") as con:
        cur = con.cursor()
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from mytable where city= ?",[zone])
        rows = cur.fetchall()
        for row in rows:
            speech_text.append(row[0])
    con.close()
    speech="The candidates for skill  "+zone+ "  are :  " + "{}.".format('\n '.join(speech_text))        
            
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
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    #
    print ("Starting app on port %d" % port)
    #app.run()
    app.run(debug=True, port=port, host='0.0.0.0')
