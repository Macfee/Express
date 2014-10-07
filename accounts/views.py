# -*-coding:utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import sessions
from django.core.exceptions import ValidationError
from django.template import RequestContext
from accounts.forms import *
from django.shortcuts import render


# Processing Account's HomePage
def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    else:
        username = request.session.get('username')
        return render_to_response('Accounts/home.html', {'username':username}, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        try:
            username = User.objects.get(email = request.POST['email']).username
        except Exception, e:
            username = None
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    auth_login(request,user)
                    return HttpResponseRedirect('/accounts/home/')
                else:
                    auth_login(request,user)
                    request.session['username'] = username
                    return HttpResponseRedirect('/accounts/home/')
            else:
               return HttpResponseRedirect('/accounts/register/')
        
        else:
            return render_to_response('Accounts/login.html')
            
    return render_to_response('Accounts/login.html')

     
    
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/accounts/home/")
    