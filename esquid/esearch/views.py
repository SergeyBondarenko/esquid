import json, simplejson

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect

from .models import Esearch

# Create your views here.

# Create Esearch obj of class Esearch
Esearch = Esearch()
Esearch.init('localhost', '9200')

# Test function. Render index.html
def index(request):
    result = Esearch.searchAll('shakespeare')
    
    context = {'results_list': result}
    return render(request, 'esearch/index.html', context)


# Function for search. Return data to frontend.
def search_all(request):
    if request.is_ajax():
        result = Esearch.searchAll('shakespeare')
        data = simplejson.dumps(result)
    else:
        data = 'Server: Fail to receive ajax request!'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# Test function. Return calls to frontend.
def postmenu(request):
     if request.method == 'POST':
         if request.is_ajax():
             message = request.POST['msg']
             return HttpResponse(str(message))
         else:
             raise Exception('Server: Exception occurred. Contact the system administrator for more informations!')
     else:
         return HttpResponse('Server: Nothing to return from server!')
    
	
# Test function. Live search in Elasticsearch fields 
def livesearch(request):
    if request.is_ajax():
        msg = request.POST.get('msg', '')
        msg = msg.split('=')
        q = msg[1]

        prog_lang = ["ActionScript","AppleScript","Asp","BASIC", \
                        "C","C++`","Clojure","COBOL", \
                        "ColdFusion","Erlang","Fortran","Groovy", \
                        "Haskell","Java","JavaScript","Lisp", \
                        "Perl","PHP","Python","Ruby","Scala","Scheme"];

        result_lang = filter(lambda x: q.lower() in x.lower(), prog_lang)
        data = simplejson.dumps(result_lang)

    else:
        data = 'Server: Fail to receive ajax request'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# Autocomplete
def autocomplete(request):
    if request.is_ajax():
        msg = request.POST.get('msg', '')
        query = msg.split('=')[1]
        index = msg.split('=')[0].split('.')[0]
        key = msg.split('=')[0].split('.')[1]
        size = 30000

        #result = Esearch.searchAll('shakespeare')
        result = Esearch.autoComplete(query, key, index, size)
        data = simplejson.dumps(result)
    else:
        data = 'Server: Fail to receive ajax request'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



# Function for Free search. Return data to frontend.
def freesearch(request):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                message = request.POST['msg']
                result = Esearch.freeSearch(message)
                data = simplejson.dumps(result)
                mimetype = 'application/json'
                return HttpResponse(data, mimetype)
            except:
                raise Exception('Server: Exception occurred. Contact the system administrator for more informations!')
        else:
            return HttpResponse('Server: Fail to receive ajax request!')
    else:
        return HttpResponse('Server: Nothing to return from server!')


# Function for Logical search. Return data to frontend.
def logicalsearch(request):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                message = request.POST['msg']
                result = Esearch.logicalSearch(message)
                data = simplejson.dumps(result)
                mimetype = 'application/json'
                return HttpResponse(data, mimetype)
            except:
                raise Exception('Server: Exception occurred. Contact the system administrator for more informations!')
        else:
            return HttpResponse('Server: Fail to receive ajax request!')
    else:
        return HttpResponse('Server: Nothing to return from server!')
