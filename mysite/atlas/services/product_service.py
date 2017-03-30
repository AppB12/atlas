from django.http import HttpResponse
from django.http import HttpRequest
import pandas as pd
import numpy as np
from atlas import static_data
#from atlas.PyScripts import ATLAS1
import datetime
import pandas as pd
import numpy as np
from atlas.PyScripts import task1
from atlas.config import dbConfig


def fetchRequests():
    df = pd.read_csv(dbConfig.dict["requestUrl"])
    jsonData = df.to_json(orient='records')
    return jsonData


def raiseRequest(request, refreshStatus):
    responseObject = {}
    keyObject = ["message", "status", "body"]
    curTime = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p")
    for i in keyObject:
        responseObject[i] = None

    columns = ['reqKw', 'reqTime', 'reqStatus']
    status = 'Pending'
    df = pd.read_csv(dbConfig.dict["requestUrl"])
    if refreshStatus:
        print refreshStatus
        if ((df['reqStatus'] == 'Pending') & (df['reqKw'] == request)).any():
            responseObject["message"] = "Conflict: A pending/processing entry for the product already exists"
            responseObject["status"] = 409
            responseObject["body"] = request
            return responseObject
        df.ix[(df.reqStatus == 'Completed') & (df.reqKw == request), 'reqTime'] = curTime
        df.ix[(df.reqStatus == 'Completed') & (df.reqKw == request), 'reqStatus'] = status
        with open(dbConfig.dict["requestUrl"], 'w') as f:
            (df).to_csv(f, index=False)
        f.close()
    else:
        # df.to_csv("C:\\Users\\akshat.gupta\\Documents\\django-atlas\\mysite\\atlas\\database\\request.csv", mode='a', index=False, sep=',', header=False)
        data = np.array([[request, curTime, status]])
        df1 = pd.DataFrame(data, columns=columns, index=[len(df)])
        with open(dbConfig.dict["requestUrl"], 'a') as f:
            (df1).to_csv(f, header=False)
        f.close()
    #task.work()
    task1.pool_exe(request)
    responseObject["message"] = "Success: Request raised successfully"
    responseObject["status"] = 200
    responseObject["body"] = request
    return responseObject


def getMetaDataFromProducts():
    ls = []
    for key, val in static_data.products.items():
        ls.append(val["metaData"])
    return ls

def uploadFile(request):
    responseObject = {}
    keyObject = ["message", "status", "body"]
    for i in keyObject:
        responseObject[i] = None
    print "Content-Type: text/html"
    print 'start!'
    a = request.FILES
    print(a)
    #print (type(a))
    #print dir(request)
    #print(dir(a['kartik-input-711[]']))
    # form = cgi.FieldStorage()

    curTime = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p")
    columns = ['reqKw', 'reqTime', 'reqStatus']
    status = 'Pending'
    df = pd.read_csv(dbConfig.dict["requestUrl"])

    if request.FILES['input44[]']:
        filedata = request.FILES['input44[]']
        if filedata.file:  # field really is an upload
            target = "../mysite/atlas/database/uploads/" + filedata._name
            with file(target, 'w') as outfile:
                outfile.write(filedata.file.read())
                responseObject["message"] = "Success: File Uploaded successfully"
                responseObject["status"] = 200
                responseObject["body"] = filedata._name

                #open requests file and raise a request to analyse this file
                data = np.array([[filedata._name, curTime, status]])
                df1 = pd.DataFrame(data, columns=columns, index=[len(df)])
                with open(dbConfig.dict["requestUrl"], 'a') as f:
                    df1.to_csv(f, header=False)
                f.close()
                task1.pool_exe_file(filedata._name)
    else:
        print '<p>No File Type selected yet</p>'
        responseObject["message"] = "Failure: Error , File NOT Uploaded"
        responseObject["status"] = 404
        responseObject["body"] = "No FILE"

    return responseObject
