from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import HttpRequest
import json
from classes.error import Error
from atlas import static_data
from atlas.services import product_service
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    return render(request, 'atlas/Search.html')


def home(request):
    return render(request, 'atlas/home.html')


def requests(request):
    return render(request, 'atlas/Requests.html')


def sentiment(request):
    return render(request, 'atlas/Sentiment.html')


# @require_http_methods(["GET"])
def searchQuery(request):
    query = request.GET['query']
    # print(static_data.products[query])

    if query in static_data.products:
        return HttpResponse(json.dumps(static_data.products[query]), status=200)
    else:
        # error = Error("product you are looking for does not exist", 404)
        # print(error)
        print("error")
        return HttpResponse("Product you are looking for does not exist", status=404)

def addProduct(request):
#    return HttpResponse("added", status=200)
    JSONdata = request.POST['name']
    responseObject = product_service.raiseRequest(JSONdata, False)
    print("Views -> add product request = ", JSONdata)
    return HttpResponse(json.dumps(responseObject), status=responseObject["status"])

def getRequests(request):
    print(product_service.fetchRequests())
    return HttpResponse(product_service.fetchRequests(), status=200)


def refreshProduct(request, product_name):
    #return HttpResponse("refreshed", status=200)
    # JSONdata = request.PUT['name']
    responseObject = product_service.raiseRequest(product_name, True)
    print("Views -> refresh product request = ", product_name)
    return HttpResponse(json.dumps(responseObject), status=responseObject["status"])


# @require_http_methods(["POST"])
# def searchQuery(request):
#     print("PUT")
#     return
#
#
# @require_http_methods(["PUT"])
# def searchQuery(request):
#     print("PUT")
#     return

def getAutoCompleteList(request):
    #return HttpResponse(json.dumps({'dict_data': static_data.product}))
    return HttpResponse(json.dumps(product_service.getMetaDataFromProducts()), status=200)

