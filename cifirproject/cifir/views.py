from re import template
from django.shortcuts import render
from django.views.generic import View
from .forms import *
from .models import *
from .forms import CreateUserForm
from itertools import chain
from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import zipfile
from lxml import etree
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 
import time
import undetected_chromedriver as chromedriver
from django.urls import reverse_lazy
from .forms import PasswordChangingForm
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.conf import settings
import csv, sys, os, django, random, datetime
from django.contrib.auth.backends import ModelBackend
from pathlib import Path

# import pathlib, pickle
# from grab import Grab
# import webbrowser
# import requests
# from bs4 import BeautifulSoup

chromedriver.TARGET_VERSION = 94
chromedriver.install()

# Create your views here.
def updateBookStatus(item, book_id):
	# revise code to add and remove from favorite, ishaveread, and istoread
	books = Book.objects.filter(id=book_id)
	if (item == "favorite"):
		isFavorite = not books[0].isFavorite
		Book.objects.filter(id=book_id).update(isFavorite=isFavorite)
	elif (item == 'have-read'):
		isHaveRead = not books[0].isHaveRead
		Book.objects.filter(id=book_id).update(isHaveRead=isHaveRead)
	elif (item == 'to-read'):
		isToRead = not books[0].isToRead
		Book.objects.filter(id=book_id).update(isToRead=isToRead)

def addToCollection(book_id, collection_id):
	print("book id: ", book_id)
	print("collection id: ", collection_id)
	book = Book.objects.get(id=book_id)
	collection = Collection.objects.get(id=collection_id)
	collection.book.add(book)

def setDriverOptions():
	options = webdriver.ChromeOptions()
	options.add_experimental_option("detach", True)

	return options

def automateLogin(username, password, url, loginBtnSelector, indicator):
	driver = webdriver.Chrome(options=setDriverOptions())
	if indicator == 1:
		driver.get(url)
		username_field = driver.find_element_by_css_selector("#username")
		username_field.send_keys(username)
		driver.execute_script("document.querySelector('#password').setAttribute('value','"+ password +"')")
		driver.execute_script("document.querySelector('"+ loginBtnSelector +"').click();")
	
	if indicator == 2:
		driver.get(url)

#CLASSES
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

		if 'updateBookStatus' in request.POST:
			updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))

		if 'addToCollection' in request.POST:
			addToCollection(request.POST.get('book_id'), request.POST.get('collection_id'))

		if 'removeFromCollection' in request.POST:
			# insert code here
			print("insert code here to remove from collection")
		return redirect('cifir:home_view')


	#pdf file format
	# def post(self, request):
	#     if request.method == 'POST':
	#     	if 'btnUpload' in request.POST:
	#     		user = User.objects.get(id=request.user.id)
	#     		#title = request.POST.get('book_title')
	# 	    	file = request.FILES.get('book_file')
	#     		a = Book( file = file)
	#     		book = Book.objects.create(file = file)
	#     		book.user.add(user)
	#     		messages.success(request,'Book added!')

	#     		return redirect('cifir:home_view')
	#     else:
	#     	messages.error(request, 'Files was not Submitted successfully!')
	#     	return redirect('cifir:home_view')

def files(request):
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('The file is saved')
    else:
        form = BookForm()
        context = {
            'form':form,
        }
    return render(request, 'base.html', context)

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

class loginPageView(View):
	def get(self, request):
		users = User.objects.all()
		print(users)
		return render(request, 'login.html')

	def post(self,request):
		if request.method == 'POST':
			if 'loginBtn' in request.POST:
				users = get_user_model()
				print('Login Button Clicked!')
				email = request.POST.get('email')
				password = request.POST.get('password')
				#user = LibUser.objects.filter(email = email,password = password)
				username = users.objects.filter(email=email)
				print(username)
				if username is not None:
					username = users.objects.get(email=email.lower()).username
					user = authenticate(username=username, password=password)
					print(user)
					if user is not None:
						login(request,user)
						request.session['email'] = email
						return redirect('cifir:home_view')
					else:
						messages.info(request, 'Email or password is incorrect')
						return redirect('cifir:login_view')
				else:
					messages.info(request, 'Email or password is incorrect')
					return redirect('cifir:login_view')
				
				# print(user)
				# if user is not None:
				# 	#user = LibUser.objects.filter(email = email,password = password)
				# 	login(request, user)
				# 	request.session['email'] = email
				# 	return redirect('cifir:home_view')
				# else:
				# 	messages.info(request, 'Email or password is incorrect')
				# 	return redirect('cifir:login_view')
			else:
			 	messages.warning(request, 'Email or password is incorrect')
			 	return render(request, 'login.html')
				
def logoutPage(request):
	logout(request)
	return redirect('cifir:login_view')


class audiobooksPageView(View):
	def get(self, request):
		return render(request,'audiobooks.html')

class profilePageView(View):
	def get(self, request):
		return render(request,'profile.html')

class PasswordChangeView(PasswordChangeView):
	form_class = PasswordChangeView
	success_url = reverse_lazy('url cifir/login_view')

class PasswordChangeDoneView(PasswordChangeDoneView):
	template_name = 'profile.html'

class PasswordResetView(View):
	def get(self, request):
		return render(request,'password_reset_form.html')

class PasswordResetDoneView(View):
	def get(self, request):
		return render(request,'password_reset_done.html')

class PasswordResetConfirmView(View):
	def get(self, request):
		return render(request,'password_reset_confirm.html')

class PasswordResetCompleteView(View):
	def get(self, request):
		return render(request,'password_reset_complete.html')

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
		catalogs = Catalog.objects.all()
		context = {
				'catalog' : catalogs,
				}
		return render(request,'networklibraries.html', context)

	def post(self, request):
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			url = request.POST.get("link")

			#convert webElement to string
			uname = str(username)
			pword = str(password)

			if "Cambridge Core" in request.POST:
				loginBtnSelector = '#login-form > div:nth-child(5) > button'
				automateLogin(username, password, url, loginBtnSelector, 1)

			elif "ProQuest Elibrary" in request.POST:
				loginBtnSelector = '#login_button'
				automateLogin(username, password, url, loginBtnSelector, 1)

			elif "Wiley Online Library" in request.POST:
				driver = webdriver.Chrome(options=setDriverOptions())
				driver.get(url)

				driver.execute_script("document.querySelector('#username').setAttribute('value','"+ username +"')")
				password = driver.find_element_by_css_selector("#password")
				password.send_keys(pword)

				driver.execute_script("document.querySelector('#main-content > div > div > div.container > div > div > div.card.card--light-shadow.login-widget.col-md-6 > div.widget__body > div.login-form > form > div.align-end > span > input').click();")

			elif "Science Direct" in request.POST:
				driver = webdriver.Chrome(options=setDriverOptions())
				driver.get(url)

				username = driver.find_element_by_css_selector("#bdd-email")
				username.send_keys(uname)
				driver.execute_script("document.querySelector('#bdd-elsPrimaryBtn').click();")
				password = driver.find_element_by_css_selector("#bdd-password")
				password.send_keys(pword)

				driver.execute_script("document.querySelector('#bdd-elsPrimaryBtn').click();")

			elif "Directory of Open Access Books" in request.POST:
				automateLogin(username, password, url, '', 2)

			elif "Zlibrary" in request.POST:
				automateLogin(username, password, url, '', 2)

			return redirect("cifir:networklibraries_view")

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
		user = User.objects.filter(username=request.user)
		collection_name = Collection.objects.filter(user=request.user).filter(name=collection)
		collection_id = Collection.objects.filter(id=collection_name)
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


# #IMPORT USERS FROM CSV

Current_Date = datetime.datetime.today().strftime ('%d-%b-%Y')
User = get_user_model()
loc1 = 'C:/accounts.csv'
loc2 = 'C:/accounts-saved'+str(Current_Date)+str(random.randint(0,100))+'.csv'
# os.rename(loc1,loc2)
file = loc1
data = csv.reader(open(file,'r'), delimiter=",")


for row in data:
    if row[1] != "Number":
        # Post.id = row[0]
        Post=User()
        usernameRow = row[3]
        userUsername = User.objects.filter(username = usernameRow).values_list('username', flat=True).first()
        print(userUsername)
        if userUsername == row[3]:
            print(userUsername)
            userUsername = User.objects.filter(username = row[3]).values('username')[0]
            finalUsername = userUsername['username']
            print("User object: " + finalUsername)
            print("Row data: " + usernameRow)
            if finalUsername == usernameRow:
                print('data are equal')
            # next(data)
        else:
	        Post.first_name = row[1]
	        Post.last_name=row[2]
	        Post.username = row[3]
	        Post.email = row[4]
	        Post.set_password(row[5])
	        # Post.last_login = "2018-09-27 05:51:42.521991"
	        Post.is_superuser = "0"
	        Post.is_staff = "1"
	        Post.is_active = "1"
	        # Post.date_joined = "2018-09-27 05:14:50"
	        print('data is saved')
	        Post.save()



# # #IMPORT USERS FROM CSV-end


