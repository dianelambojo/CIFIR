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
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import zipfile
from lxml import etree


# Create your views here.
def updateBookStatus(item, book_id):
	print(item, book_id)
	if (item == "favorite"):
		update_book = Book.objects.filter(id=book_id).update(isFavorite=True)
		#insert success message here pls hahaha		
	elif (item == 'have-read'):
		update_book = Book.objects.filter(id=book_id).update(isHaveRead=True)
		#insert success message here pls hahaha		
	elif (item == 'to-read'):
		update_book = Book.objects.filter(id=book_id).update(isToRead=True)
		#insert success message here pls hahaha		

class homePageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user).filter(isDeleted=False)
		catalog = Catalog.objects.all()
		book = Book.objects.filter(user=request.user)

		context = {
				'collections' : collection,
				'catalogs' : catalog,
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
			messages.success(request,'Book added!')

			# return render(request, 'homepage.html')
			return redirect('cifir:home_view')

		if 'updateBookStatus' in request.POST:
			updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))
			return redirect('cifir:home_view')

class loginPageView(View):
	def get(self, request):
		users = User.objects.all()
		print(users)
		return render(request, 'login.html')

	def post(self,request):
		if request.method == 'POST':
			if 'loginBtn' in request.POST:
				print('Login Button Clicked!')
				username = request.POST.get('username')
				password = request.POST.get('password')
				#user = LibUser.objects.filter(email = email,password = password)
				user = authenticate(request, username=username, password=password)
				print(user)
				if user is not None:
					#user = LibUser.objects.filter(email = email,password = password)
					login(request, user)
					request.session['username'] = username
					return redirect('cifir:home_view')
				else:
					messages.info(request, 'Email or password is incorrect')
					return redirect('cifir:login_view')
			else:
			 	messages.warning(request, 'Email or password is incorrect')
			 	return render(request, 'login.html')
				
def logoutPage(request):
	logout(request)
	return redirect('cifir:login_view')


class audiobooksPageView(View):
	def get(self, request):
		return render(request,'audiobooks.html')

class bookmarksPageView(View):
	def get(self, request):

		return render(request,'bookmarks.html')
		
class epubReadpageView(View):
	def get(self, request):
		book_id = request.POST.get('book_id', None)
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(id=book_id)

		context = {
					'books' : book,
				}

		return render(request,'EpubRead.html', context)

	def post(self,request):
		context = {}
		book_id = request.POST.get('book_id', None)
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(id=book_id)

		context = {
					'books' : book,
				}

		return render(request, 'EpubRead.html', context)

class collectionsPageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user).filter(isDeleted=False)
		context = {
				'collections' : collection,
				'users' : user,
				}
		return render(request, 'collections.html', context)

	def post(self, request):
		user = User.objects.get(id=request.user.id)
		collection_name = request.POST.get('collection_name')
		collection = Collection.objects.create(name = collection_name)
		collection.user.add(user)
		messages.success(request,'Collection Added Successfuly!')


		return redirect('cifir:collections_view')


class favoritesPageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(isFavorite=True)

		context = {
				'users' : user,
				'books' : book,
				}

		return render(request, 'favorites.html', context)


class haveReadPageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(isHaveRead=True)

		context = {
				'users' : user,
				'books' : book,
				}

		return render(request,'haveRead.html', context)

class toReadPageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(isToRead=True)

		context = {
				'users' : user,
				'books' : book,
				}

		return render(request,'toRead.html', context)

class networkLibrariesPageView(View):
	def get(self, request):
		return render(request,'networklibraries.html')

class viewBook(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user)

		context = {
				'collections' : collection,
				}
		return render(request, 'files.html', context)

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
			if 'editCollectionBtn' in request.POST:
				print('clicked')
				collection_new_name = request.POST.get("name")
				collection_id = request.POST.get("id")
				print(collection_new_name)
				update_collection = Collection.objects.filter(id=collection_id).update(name=collection_new_name)
				print('save')

				messages.success(request,'Collection Edited Successfuly!')

			elif 'deleteCollectionBtn' in request.POST:	

				print('Delete Button Clicked')
				collection_id = request.POST.get("id")
				collection = Collection.objects.filter(id = collection_id).update(isDeleted=True)
				print('Collection Deleted')

				messages.success(request,'Collection Deleted Successfuly!')

		return render(request, 'files.html', context)


