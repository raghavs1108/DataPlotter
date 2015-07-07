from bottle import Bottle, request, response, run

import pymysql
import sys

conn = pymysql.connect(db="stepdata",host='localhost', user='root', passwd='cdac123')
conn.autocommit(True)
cur = conn.cursor()

index = 0;
app = Bottle()
 
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
msec = 0;

def getTime(time):
    global msec;
    date, time = time.split(";");
    date = date.split(":");
    time = time.split(":");
    sec, msec = time[2].split(".");
    time = date[2]+"-"+date[1]+"-"+date[0]+" "+time[0]+":"+time[1]+":"+sec;
    return time

def saveData(values):
    stringToWrite = "";
    for x in values:
        query = "";
        query+= str(x[0]) + ",";
        query+= str(x[1]) + ",";
        query+= str(x[2]) + ",";
        query+= str(x[3]) + ",";
        query+= str(x[4]) + ",";    
        query+= str(x[5]) + ",";    
        query+= str(x[6]) + ",";    
        query+= str(x[7]) + ",";    
        query+= str(x[8]) + ",";    
        query+= str(x[9]) + ",";    
        query+= str(x[10]) + ",";    
        query+= str(x[11]) + ",";    
        query+= (x[12]);
        stringToWrite += query + "\n"

    f = open("data.txt", "w")
    f.write(stringToWrite)
    f.close()

 
@app.route('/test/', method=['OPTIONS', 'POST'])
def examples():
   return "Success."

@app.route('/data', method=['OPTIONS', 'POST'])
def dataStorage():
    values = request.body.read()
    values = request.forms
    allValues = []
    count = 0
    for i in values:
        allValues += [request.forms.get("stepdata"+str(count))]
        count+=1

    allData = [];
    data = [None]*13;
    for i in allValues:
        values = i.split("&")
        for j in values:
            x = j.split("=")
            if x[0] == "step":
                data[0] = x[1]
            elif x[0] == "stepLength":
                data[1] = x[1]
            elif x[0] == "stepAngle":
                data[2] = x[1]
            elif x[0] == "xAcc":
                data[3] = x[1]
            elif x[0] == "yAcc":
                data[4] = x[1]
            elif x[0] == "zAcc":
                data[5] = x[1]
            elif x[0] == "phoneXAcc":
                data[6] = x[1]
            elif x[0] == "phoneYAcc":
                data[7] = x[1]
            elif x[0] == "phoneZAcc":
                data[8] = x[1]
            elif x[0] == "min1":
                data[9] = x[1]
            elif x[0] == "min2":
                data[10] = x[1]
            elif x[0] == "max1":
                data[11] = x[1]
            elif x[0] == "time":
                data[12] = x[1]

        allData.append(data)
    saveData(allData)

    # print(data)
    
    return "values"

if __name__ == '__main__':
    from optparse import OptionParser
    
    host = "10.182.1.14";
    port = 8080;
    run(app, host=host, port=port)