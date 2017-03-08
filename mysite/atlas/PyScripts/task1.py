from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import subprocess

from time import sleep
import ATLAS1


def return_after_5_secs(request):
    print("Entering", [request])
    ATLAS1.main([request])
    '''
        status = atlas.scrape(product_name)
        if(status == 200 || 404) then update request csv status to completed
        else set t0 failed
    '''
    print("Exiting return")
    return request


pool = ProcessPoolExecutor()
def pool_exe(request):
    future = pool.submit(return_after_5_secs, request)
    print ("exit pool exe\n")
