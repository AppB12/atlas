#!/usr/bin/python

import os
import commands
import cgi, cgitb
from django.http import HttpResponse

def upload(request):
    cgitb.enable()
    print "Content-Type: text/html"
    print
    print 'start!'
    print dir(request)
    print(type(request._files['upload'].file))


    #form = cgi.FieldStorage()
    if request._files['upload']:
        filedata = request._files['upload']
        if filedata.file: # field really is an upload
            with file("data.csv", 'w') as outfile:
                outfile.write(filedata.file.read())
        return HttpResponse("Upload succesful", status=200)
    else:
        print '<p>No File Type selected yet</p>'
        return HttpResponse("Upload unsuccesful", status=404)