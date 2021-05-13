from django.shortcuts import render
from django.views.generic import View
from .forms import *
from .models import *
from .forms import CreateUserForm
from itertools import chain
from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class indexView(View):
	def get(self, request):
		return render(request,'index.html')

class homePageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		library = Library.objects.exclude(user=request.user)
		collection = Collection.objects.filter(user=request.user)
		catalog = Catalog.objects.all()
		context = {
				'collections' : collection,
				'catalogs' : catalog,
				'libraries' : library,
				'users' : user,
				}

		return render(request, 'homepage.html', context)

class loginPageView(View):
	def get(self, request):
		return render(request,'login.html')
	def post(self,request):
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		print(user)


		if user is not None:
			login(request, user)
			# pass the name of the user to the base.html navbar
			request.session['username'] = username
			return redirect('cifir:home_view')
		else:
			messages.info(request, 'Username or password is incorrect')
				
		return render(request, 'login.html')


class audiobooksPageView(View):
	def get(self, request):
		return render(request,'audiobooks.html')

class bookmarksPageView(View):
	def get(self, request):
		return render(request,'bookmarks.html')

class collectionsPageView(View):
	def get(self, request):
		return render(request,'collections.html')

class favoritesPageView(View):
	def get(self, request):
		return render(request,'favorites.html')

class haveReadPageView(View):
	def get(self, request):
		return render(request,'haveRead.html')

class toReadPageView(View):
	def get(self, request):
		return render(request,'toRead.html')

class networkLibrariesPageView(View):
	def get(self, request):
		return render(request,'networklibraries.html')

class filesView(View):
	def get(self,request):
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user)
		book = Book.objects.filter(collection=True)
		context = {
				'collections' : collection,
				'books' : book,
				'users' : user,
				}

		return render(request, 'files.html', context)