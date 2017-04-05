from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import pymongo
import datetime
import binascii
from time import sleep
import ATLAS1
from atlas.config import dbConfig
import pandas as pd
import SentimentAPI
import SentimentAPI_generic
import TrigDriv


def caller_file(request):
    print("Entering File analysis", request)
    db = pymongo.MongoClient().atlas
    s = request.encode('utf-8')
    file_dict = {
        '_id': binascii.hexlify(s),
        'Product': request,

        'metadata': {
            '_id': binascii.hexlify(s),
            'lastUpdated': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p"),
            'name': request
        },
        'analyticData': {
            'sentimentData': [

            ],
            'trigdrivData': [

            ]
        }
    }
    result = db.data.insert_one(file_dict)
    sent_list = SentimentAPI_generic.senti_main(dbConfig.dict['uploadsUrl'] + request, ',')
    print sent_list

    target_string = "analyticData.sentimentData"

    db.data.update({"_id": binascii.hexlify(s)}, {"$set": {target_string: sent_list[0]}})
    print result.inserted_id
    print("Exiting return")
    return request


def caller(request):
    print("Entering", request)

    db = pymongo.MongoClient().atlas
    s = request.encode('utf-8')
    status = ATLAS1.main(request)
    prod_dict = {
        '_id': binascii.hexlify(s),
        'Product': request,
        'metadata': {
            '_id': binascii.hexlify(s),
            'lastUpdated': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p"),
            'name': request
        },
        'analyticData': {
            'sentimentData': [

            ],
            'trigdrivData': [

            ],
        }
    }
    result = db.data.insert_one(prod_dict)
    print("Atlas main finish")

    df = pd.read_csv(dbConfig.dict["requestUrl"])

    '''
    if(status == 200):
        #Update request csv status to completed
        sent_list = []
        sent_list = SentimentAnalysis.senti_main(dbConfig.dict['outputUrl'], request)
        print sent_list
        df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Completed"
    else:
        df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Failed"

    with open(dbConfig.dict["requestUrl"], 'w') as f:
        (df).to_csv(f, index=False)
    '''
    sent_list = []
    sent_list = SentimentAPI.senti_main(dbConfig.dict['outputUrl'], request)
    print sent_list

    target_string = "analyticData.sentimentData"

    db.data.update({"_id": binascii.hexlify(s)}, {"$set": {target_string: sent_list[0]}})
    print result.inserted_id
    print("Exiting return")
    return request


pool = ProcessPoolExecutor()
def pool_exe(request):
    future = pool.submit(caller, request)
    print ("Exit pool exe\n")

def pool_exe_file(request):
    future = pool.submit(caller_file, request)
    print("Exit file pool exe\n")
