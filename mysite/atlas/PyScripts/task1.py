from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

from time import sleep
import ATLAS1
from atlas.config import dbConfig
import pandas as pd
import SentimentAPI
import TrigDriv


def caller(request):
    print("Entering", request)

    status = ATLAS1.main(request)
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
    print("Exiting return")
    return request


pool = ProcessPoolExecutor()
def pool_exe(request):
    future = pool.submit(caller, request)
    print ("Exit pool exe\n")
