from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from luminoso_api import LuminosoClient

import time
import json
import os
import pickle

# get pw from hidden file, TBD: figure out how to get EC2 instance env variables set
pw = ""
fname = os.path.abspath('../')+'/.env'  # local file
if os.path.isfile(fname):
    pw = open(fname, 'r').read()[:16]
fname = '/home/ubuntu/.env'             # ec2 file
if os.path.isfile(fname):
    pw = open(fname, 'r').read()[:16]

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')

    return render(request, 'search_form.html')


def connect_client(project_name):
#   client connection
    client = LuminosoClient.connect('/projects/t55y685c/', username='zynga@luminoso.com', password=pw)
    project = client.get(name=project_name)[0]
    project = client.change_path(project['project_id'])
    return project

def load_project(language, request):

    # handle all available languages
    if language == 'English':
        project_name = "Zynga - English"
    elif language == 'French':
        project_name = "Zynga - French"
    elif language == 'Italian':
        project_name = "Zynga - Italian"
    elif language == 'German':
        project_name = "Zynga - German"
    elif language == 'Spanish':
        project_name = "Zynga - Spanish"
    elif language == 'Portuguese':
        project_name = "Zynga - Portuguese"
    elif language == 'Japanese':
        project_name = "Zynga - Japanese"
    elif language == 'Chinese':
        project_name = "Zynga - Chinese"

    if request.session[project_name] == "Empty":
    # create project reference and add to session vars
        project = connect_client(project_name)
        request.session[project_name] = pickle.dumps(project)
    else:
    # load project reference from session vars
        project = pickle.loads(request.session[project_name])
        try:   # make sure project reference is still good
            test = project.change_path('/')
            test.get('ping')
        except:
            project = connect_client(project_name)
            request.session[project_name] = pickle.dumps(project)

    return project


def conceptual_search(question, language, request):

    if len(question) <0:    # use to limit question length
        return "Empty"

    results = {}   # dict of search results
    matches = []   # list of search matches

    project = load_project(language, request)

    millis_before = int(round(time.time() * 1000))
    search = project.get('docs/search/', text=question, limit=35)
    millis_after = int(round(time.time() * 1000))
    for i,match in enumerate(search['search_results']):
         key = "result %s" % i
         matches.append(match[0]['document']['text'])

    results["time"] = (millis_after - millis_before)  # search time
    results["matches"] = matches  # search matches
    return results

def search(request):
    # force authenticated user
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')

    if 'question' in request.GET:
        results = conceptual_search(request.GET['question'], request.GET['language'], request)

        if results != "Empty":
            args = {}
            args['question'] = request.GET['question']
            args['language'] = request.GET['language']
            args['time'] = results["time"]
            args['results'] = results["matches"]
            return render_to_response("search_form.html", args)
        else:
            return HttpResponseRedirect("/")

    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)

#        import pdb; pdb.set_trace()


