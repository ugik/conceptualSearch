from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail

import logging
logr = logging.getLogger(__name__)

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')

    context = {}
    return render_to_response('index.html', context, context_instance=RequestContext(request))	

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c, context_instance=RequestContext(request))

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
	
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/user/loggedin')
    else:
        return HttpResponseRedirect('/user/invalid')

def loggedin(request):
    # clear out all session objects to projects
    request.session['Zynga - English'] = "Empty"
    request.session['Zynga - French'] = "Empty"
    request.session['Zynga - Italian'] = "Empty"
    request.session['Zynga - German'] = "Empty"
    request.session['Zynga - Spanish'] = "Empty"
    request.session['Zynga - Portuguese'] = "Empty"
    request.session['Zynga - Japanese'] = "Empty"
    request.session['Zynga - Chinese'] = "Empty"

    return render_to_response('loggedin.html',
						 	 {'full_name' : request.user.username},
							  context_instance=RequestContext(request))

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/user/register_success')

	args = {}
	args.update(csrf(request))
	
	args['form'] = UserCreationForm()
	return render_to_response('register.html', args)

def register_success(request):
	return render_to_response('register_success.html')


