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
import zipfile
from lxml import etree

import ebooklib
from ebooklib import epub
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
		book = Book.objects.filter(user=request.user)

		context = {
				'collections' : collection,
				'catalogs' : catalog,
				'libraries' : library,
				'users' : user,
				'books' : book,
				}

		return render(request, 'homepage.html', context)

	def post(self,request):
		if 'btnUpload' in request.POST:
			user = User.objects.get(id=request.user.id)
			file = request.FILES.get('book_file')
			print(file)
			ns = {
			        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
			        'pkg':'http://www.idpf.org/2007/opf',
			        'dc':'http://purl.org/dc/elements/1.1/'
			    }

			zip = zipfile.ZipFile(file)

			txt = zip.read('META-INF/container.xml')
			tree = etree.fromstring(txt)
			cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

			    # grab the metadata block from the contents metafile
			cf = zip.read(cfname)
			tree = etree.fromstring(cf)
			p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

			    # repackage the data
			res = {}
			for s in ['title','language','creator','date','identifier']:
				res[s] = p.xpath('dc:%s/text()'%(s),namespaces=ns)[0]
			print(res['title'])
			book = Book.objects.create(title= res['title'], file = file)
			book.user.add(user)

			return HttpResponse('Book uploaded!')

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
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user)
		context = {
				'collections' : collection,
				'users' : user,
				}
		return render(request, 'collections.html', context)

	def post(self, request):
		user = User.objects.get(id=request.user.id)
		collection_name = request.POST.get('collection_id')
		collection = Collection.objects.create(name = collection_name)
		collection.user.add(user)

		return HttpResponse('Collection added!')


		return redirect('cifir:collection_view')


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

class viewBook(View):
	def post(self,request):
		context = {}
		collection = request.POST.get('collection', None)
		collection_id = request.POST.get('collection_id', None)
		user = User.objects.filter(username=request.user)
		collection_name = Collection.objects.filter(user=request.user).filter(name=collection)
		book = Book.objects.filter(user=request.user)

		context = {
					'collections' : collection,
					'collection_names' : collection_name,
					'books' : book,
				}

		if request.method == 'POST':	
			if 'btnEdit' in request.POST:	
				print('clicked')
				collection_new_name = request.POST.get("collection_name")
				collection_id = request.POST.get("collection_id")
				update_collection = Collection.objects.filter(id = collection_id).update(name=collection_new_name)

				return HttpResponse('Collection edited!')

		return render(request, 'files.html', context)


