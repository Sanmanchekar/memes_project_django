from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import requests

# Create your views here.

from .models import *
from .forms import CreateUserForm
import datetime
from datetime import timedelta


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
    	form = CreateUserForm(request.POST)
    	if form.is_valid():
    		form.save()
    		# messages.success(request, 'Account was created for' + user)
    		# user = form.cleaned_data.get('username')
 
    		return redirect('login')

    context = {'form':form}
    return render(request, 'memes/register.html', context)

@csrf_protect
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			response = render(request, 'memes/webpage.html')
			response.set_signed_cookie('user', user, salt='nm', expires=datetime.datetime.utcnow()+timedelta(days=2))
			response.set_cookie('last_connection', datetime.datetime.now())
			response.set_cookie('username', datetime.datetime.now())
			return redirect('webpage')
		else:
			messages.info(request, 'Username or password is incorrect')

	context = {}
	return render(request, 'memes/login.html', context)


def logoutPage(request):
	logout(request)
	response = render(request, 'memes/login.html')
	response.delete_cookie('name')
	return redirect('login')


def webpage(request):
	# get current user
	current_user = request.user
	# print(current_user.username)

	# get cookies
	name = request.get_signed_cookie(current_user.username, default='Guest', salt='nm')
	context = {
		'cookie_data' : request.COOKIES,
		'last_connection': datetime.datetime.now(),
		'username': current_user.username,
		'email': current_user.email,
	}

	# api
	response = requests.get('https://api.imgflip.com/get_memes')
	data = response.json()

	memesObj = data['data']['memes']

	memesList = []
	for index,data in enumerate(memesObj):
		memesList.append(data)
		print(index,data)
		if index==4:
			break

	# logout
	if request.method == "POST":
		logout(request)

		return redirect('home')

	print("##################################")
	print(context['cookie_data']['sessionid'])
	print(context['username'])
	print(context['email'])
	print(context['last_connection'])
	
	return render(request, 'memes/webpage.html', {'name':name, 'memes':memesList, 'context':context})

