import django
django.setup()
from re import template
from .forms import *
from .models import *
from .forms import CreateUserForm, PasswordChangingForm
from itertools import chain
from django.views.generic import View
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, auth
from django.contrib import messages, admin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q 

#tts
import pyttsx3
import multiprocessing as mp
import urllib3
import io
#pdf
import pdfplumber
import keyboard

#epub
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup

#epub metadata, book cover etc
from lxml import etree
import zipfile
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

#automate login
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 
import time
import undetected_chromedriver as chromedriver
import csv, sys, os, django, random
from datetime import datetime
from pathlib import Path
import os

from splinter import Browser

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chromedriver.TARGET_VERSION = 96
chromedriver.install()


#API
import collections
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from rest_framework.decorators import APIView

from cifir.serializers import CollectionSerializer, CreateUserSerializer, UserSerializer

from cifir.serializers import BookSerializer

from .models import *


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
	print('book added')

def automateLoginToSite(request, username, password, url, loginBtnSelector, indicator):
	global browser
	browser = Browser('chrome')
	if indicator == 1:
		try:
			browser.visit(url)
			browser.find_by_css("#username").fill(username)
			browser.find_by_css("#password").fill(password)
			browser.find_by_css(loginBtnSelector).click()
		except:
			messages.success(request,'Failed to access the database. Try Again Later.')
	if indicator == 2:
		try:
			browser.visit(url)
		except:
			messages.success(request,'Failed to access the database. Try Again Later.')


def epubtotext(bookFile):
	bookFile = bookFile

	url = "https://cifirstorage.blob.core.windows.net/media/" + bookFile
	print(url)

	http = urllib3.PoolManager()
	temp = io.BytesIO()
	temp.write(http.request("GET", url).data)
	print(temp)

	book = epub.read_epub(temp)

	for item in book.get_items():
		if item.get_type() == ebooklib.ITEM_DOCUMENT:
			soup = BeautifulSoup(item.get_body_content(), 'html.parser')
			text = [para.get_text() for para in soup.find_all('p')]
			txt = soup.text.replace('\n', '' '').strip()
			tts(txt)
	
def pdftotext(bookFile,currentPage):

	bookFile = bookFile
	currentPage = int(currentPage)
	print(bookFile)
	print('tts activated')
	print(currentPage)

	url = "https://cifirstorage.blob.core.windows.net/media/" + bookFile
	print(url)

	http = urllib3.PoolManager()
	temp = io.BytesIO()
	temp.write(http.request("GET", url).data)
	print(temp)

	with pdfplumber.open(temp) as pdf:
		text = pdf.pages[currentPage].extract_text()
		tts(text)

	# pdf = pdfplumber.open(path)

	# #1 page only
	# page = pdf.pages[currentPage]
	# text = page.extract_text()
	# tts(text)

	# start from currentpage until sa mga next
	# totalpages = len(pdf.pages)
	# for i in range(currentPage, totalpages ):
	#     page = pdf.pages[i]
	#     page_content = page.extract_text()
	# tts(page_content)


def tts(text):
	
	p = mp.Process(target=speak, args=(text,))
	p.start()
	while p.is_alive():
		if keyboard.is_pressed('spacebar'):
			p.terminate()
		else:
			continue
	p.join()

def speak(text):
	speak = pyttsx3.init('sapi5')
	voices = speak.getProperty('voices')
	speak.setProperty("rate", 178)
	speak.setProperty("voice", voices[0].id)
	speak.say(text)
	speak.runAndWait()


#CLASSES
class homePageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user).filter(isDeleted=False)
		catalogs = Catalog.objects.all()
		book = Book.objects.filter(user=request.user)

		context = {
				'collections' : collection,
				'catalog' : catalogs,
				'users' : user,
				'books' : book,
				}

		return render(request, 'homepage.html', context)

	def post(self,request):
		if request.method == "POST":
			#NETWORK LIBRARIES
			username = request.POST.get("username")
			password = request.POST.get("password")
			url = request.POST.get("link")

			#convert webElement to string
			uname = str(username)
			pword = str(password)

			if "Cambridge Core" in request.POST:
				loginBtnSelector = '#login-form > div:nth-child(5) > button'
				automateLoginToSite(request, username, password, url, loginBtnSelector, 1)
				return redirect('cifir:home_view')

			elif "ProQuest Elibrary" in request.POST:
				loginBtnSelector = '#login_button'
				automateLoginToSite(request, username, password, url, loginBtnSelector, 1)
				return redirect('cifir:home_view')

			elif "Wiley Online Library" in request.POST:
				loginBtnSelector = '#main-content > div > div > div.container > div > div > div.card.card--light-shadow.login-widget.col-md-6 > div.widget__body > div.login-form > form > div.align-end > span > input'
				automateLoginToSite(request, username, password, url, loginBtnSelector, 1)
				return redirect('cifir:home_view')

			elif "Science Direct" in request.POST:
				global browser
				browser = Browser('chrome')
				try:
					browser.visit(url)
					browser.find_by_css("#bdd-email").fill(username)
					browser.find_by_css('#bdd-elsPrimaryBtn').click()
					browser.find_by_css("#bdd-password").fill(password)
					browser.find_by_css('#bdd-elsPrimaryBtn').click()
				except:
					messages.success(request,'Failed to access the database. Try Again Later.')

				return redirect('cifir:home_view')

			elif "Directory of Open Access Books" in request.POST:
				automateLoginToSite(request, username, password, url, '', 2)
				return redirect('cifir:home_view')

			elif "Zlibrary" in request.POST:
				automateLoginToSite(request, username, password, url, '', 2)
				return redirect('cifir:home_view')
			
			#UPLOAD BOOK
			if 'btnUpload' in request.POST:
				user = User.objects.get(id=request.user.id)
				file = request.FILES.get('book_file')
				ext = os.path.splitext(file.name)[1]  # [0] returns path+filename
				epub_extensions = ['.epub']
				pdf_extensions = ['.pdf']

				#EPUB FILE FORMAT
				if ext.lower() in epub_extensions: 
					print(file)
					print('')
		
					namespaces = {
					   "calibre":"http://calibre.kovidgoyal.net/2009/metadata",
					   "dc":"http://purl.org/dc/elements/1.1/",
					   "dcterms":"http://purl.org/dc/terms/",
					   "opf":"http://www.idpf.org/2007/opf",
					   "u":"urn:oasis:names:tc:opendocument:xmlns:container",
					   "xsi":"http://www.w3.org/2001/XMLSchema-instance",
					   'pkg':'http://www.idpf.org/2007/opf',
					}

					zip = zipfile.ZipFile(file)
					t = etree.fromstring(zip.read("META-INF/container.xml"))

					for i in t:
						print(i)
					print('')
					rootfile_path =  t.xpath("/u:container/u:rootfiles/u:rootfile",namespaces=namespaces)[0].get("full-path")
					t = etree.fromstring(zip.read(rootfile_path))
					
					p = t.xpath('/pkg:package/pkg:metadata',namespaces=namespaces)[0]
						
					# repackage the data
					res = {}
					for s in ['title','language','creator','date','identifier']:
						 res[s] = p.xpath('dc:%s/text()'%(s),namespaces=namespaces)[0]
				
					try:
						cover_id = t.xpath("//opf:metadata/opf:meta[@name='cover']",namespaces=namespaces)[0].get("content")
						cover_href = t.xpath("//opf:manifest/opf:item[@id='" + cover_id + "']",namespaces=namespaces)[0].get("href")
						cover_path = os.path.join(os.path.dirname(rootfile_path), cover_href)

						image = Image.open(zip.open(cover_path))
						image_io = BytesIO()
						image.save(image_io, format='png', quality=100) # you can change format and quality
						# save to model
						image_name = "cover"
						book = Book.objects.create(title= res['title'], file = file, book_author=res['creator'])
						book.user.add(user)
						book.cover.save(image_name, ContentFile(image_io.getvalue()))

					except KeyError:
						book = Book.objects.create(title= res['title'], file = file, book_author=res['creator'], cover="media/epub_cover_default.png")
						book.user.add(user)
						messages.success(request,'Book added!')
					
					return redirect('cifir:home_view')

				if ext.lower() in pdf_extensions:
					#PDF FILE FORMAT
					book = Book.objects.create(title= file.name, file = file, cover="media/pdf_cover_default.png")
					book.user.add(user)
					messages.success(request,'PDF added!')
				
				return redirect('cifir:home_view')

			if 'updateBookStatus' in request.POST:
				updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))
				messages.success(request,"Book updated!")
				return redirect('cifir:home_view')
			if 'addToCollection' in request.POST:
				print('hi there')
				addToCollection(request.POST.get('book_id'), request.POST.get('collection_id'))
				return redirect('cifir:collections_view')
			if 'removeFromCollection' in request.POST:
				# insert code here
				print("insert code here to remove from collection")

			return redirect('cifir:home_view')

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
		return render(request, 'index.html')


	def post(self,request):
		if request.method == 'POST':
			if 'loginBtn' in request.POST:
				users = get_user_model()
				print('Login Button Clicked!')
				email = request.POST.get('email')
				password = request.POST.get('password')
				username = users.objects.filter(email=email)
				print(username)
				#if username is not None:
				username = users.objects.get(email=email.lower()).username
				user = authenticate(username=username, password=password)
				print(user)
					
				if user is not None:
					login(request,user)
					request.session['email'] = email

					if request.user.is_superuser:
						return redirect('cifir:admin_view')
					elif user.check_password(123456):
						messages.success(request,"Logged in successfully")
						messages.info(request, "Please reset your password in Account Setting.")
						return redirect('cifir:home_view')
					else:
						messages.success(request,"Logged in successfully")
						return redirect('cifir:home_view')
				else:
					messages.info(request, 'Email or password is incorrect')
					return redirect('cifir:login_view')
			
			else:
				messages.warning(request, 'Email or password is incorrect')
				return render(request, 'index.html')
			
def logoutPage(request):
	logout(request)
	return redirect('cifir:login_view')


class adminPageView(View):
	def get(self, request):
		user = User.objects.all()
		catalog = Catalog.objects.all()

		context = {
				'users' : user,
				'catalogs' : catalog,
				}
		return render(request,'admin/admin.html', context)


class profilePageView(View):
	def get(self, request):
		return render(request,'profile.html')

class PasswordChangeView(PasswordChangeView):
	form_class = PasswordChangeView
	success_url = reverse_lazy('url cifir/login_view')

class PasswordChangeDoneView(PasswordChangeDoneView):
	template_name = 'profile.html'

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
		if request.method == "POST":
			book_id = request.POST.get('book_id', None)
			user = User.objects.filter(username=request.user)
			book = Book.objects.filter(user=request.user).filter(id=book_id)
			
			numlist=[]
			bookmarks = Bookmark.book.through.objects.filter(book_id=book_id)
			for b in bookmarks:
				x = b.book_id
				numlist.append(b.bookmark_id)

			allBookmarks = Bookmark.objects.filter(Q(id__in=numlist))

			if allBookmarks.exists():
				context = {
							'books' : book,
							'allBookmarks': allBookmarks,
							'currentPage': allBookmarks.order_by('-id')[0].bookpage,
						}
			else:
				context = {
							'books' : book,
							'allBookmarks': allBookmarks,
						}

			if 'tts-btn' in request.POST:
				bookFile = request.POST.get('bookFile')
				print(bookFile)
				print('read request')
				epubtotext(bookFile)
				return render(request, 'EpubRead.html', context)
			

			if 'add-bookmark' in request.POST:
				currentBook = request.POST.get('currentBook', None)
				bookmark = request.POST.get('bookmarkId')
				index = request.POST.get('bookmarkIndex')
				
				bookId = Book.objects.get(id=currentBook)

				checkList=[]
				bookId = Book.objects.get(id=currentBook)

				getBookmarks = Bookmark.objects.filter(book=bookId.id)
				for mark in getBookmarks:
					checkList.append(mark.bookpage)

				if bookmark in checkList:
					user = User.objects.filter(username=request.user)
					book = Book.objects.filter(user=request.user).filter(id=currentBook)

					numlist=[]
					bookmarks = Bookmark.book.through.objects.filter(book_id=currentBook)
					for b in bookmarks:
						numlist.append(b.bookmark_id)

					allBookmarks = Bookmark.objects.filter(Q(id__in=numlist))

					latest = Bookmark.objects.filter(Q(id__in=numlist)).last().bookpage

					context = {
						'books' : book,
						'allBookmarks': allBookmarks,
						'currentPage': latest,
					}
				else:
					bmark = Bookmark(bookpage=bookmark, page_index = index)
					bmark.save()
					bmark.book.add(currentBook)
			return render(request, 'EpubRead.html', context)

				# with requests.Session() as s:
				# 	s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
				# 	r = s.get('https://httpbin.org/cookies')
				# https://www.py4u.net/discuss/22338
				# return render(request, 'EpubRead.html')

		return render(request, 'EpubRead.html', context)

class pdfReadpageView(View):
	def get(self, request):
		book_id = request.POST.get('book_id', None)
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(id=book_id)

		context = {
					'books' : book,
				}

		return render(request,'PDFRead.html', context)

	def post(self,request):
		if request.method == "POST":
			# context = {}
			book_id = request.POST.get('book_id', None)
			user = User.objects.filter(username=request.user)
			book = Book.objects.filter(user=request.user).filter(id=book_id)

			numlist=[]
			bookmarks = Bookmark.book.through.objects.filter(book_id=book_id)
			for b in bookmarks:
				numlist.append(b.bookmark_id)

			allBookmarks = Bookmark.objects.filter(Q(id__in=numlist))

			if allBookmarks.exists():
				context = {
							'books' : book,
							'allBookmarks': allBookmarks,
							'currentPage': allBookmarks.order_by('-id')[0].bookpage,
						}
			else:
				context = {
							'books' : book,
							'allBookmarks': allBookmarks,
						}

			if 'tts-btn' in request.POST:
				bookFile = request.POST.get('bookFile')
				currentPage = request.POST.get('currentpage')
				print(bookFile)
				print(currentPage)
				print('read request')
				pdftotext(bookFile,currentPage)

			if 'add-bookmark' in request.POST:
				currentBook = request.POST.get('currentBook', None)
				bookmark = request.POST.get('bookmarkId')

				checkList=[]
				bookId = Book.objects.get(id=currentBook)

				getBookmarks = Bookmark.objects.filter(book=bookId.id)
				for mark in getBookmarks:
					checkList.append(mark.bookpage)

				if bookmark in checkList:
					user = User.objects.filter(username=request.user)
					book = Book.objects.filter(user=request.user).filter(id=currentBook)

					numlist=[]
					bookmarks = Bookmark.book.through.objects.filter(book_id=currentBook)
					for b in bookmarks:
						numlist.append(b.bookmark_id)

					allBookmarks = Bookmark.objects.filter(Q(id__in=numlist))

					latest = Bookmark.objects.filter(Q(id__in=numlist)).last().bookpage

					context = {
						'books' : book,
						'allBookmarks': allBookmarks,
						'currentPage': latest,
					}
					
				else:
					bmark = Bookmark(bookpage=bookmark, page_index = bookmark)
					bmark.save()
					bmark.book.add(currentBook)
			return render(request, 'PDFRead.html', context)

		return render(request, 'PDFRead.html', context)

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
		messages.success(request,'Collection Added Successfully!')


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

	def post(self, request):
		if request.method == "POST":
			if 'updateBookStatus' in request.POST:
					updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))
					return redirect('cifir:favorites_view')



class haveReadPageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(isHaveRead=True)

		context = {
				'users' : user,
				'books' : book,
				}

		return render(request,'haveRead.html', context)

	def post(self, request):
		if request.method == "POST":
			if 'updateBookStatus' in request.POST:
					updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))
					return redirect('cifir:haveread_view')

class toReadPageView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(isToRead=True)

		context = {
				'users' : user,
				'books' : book,
				}

		return render(request,'toRead.html', context)

	def post(self, request):
		if request.method == "POST":
			if 'updateBookStatus' in request.POST:
					updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))
					return redirect('cifir:toread_view')

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
				automateLoginToSite(request, username, password, url, loginBtnSelector, 1)

			elif "ProQuest Elibrary" in request.POST:
				loginBtnSelector = '#login_button'
				automateLoginToSite(request, username, password, url, loginBtnSelector, 1)

			elif "Wiley Online Library" in request.POST:
				loginBtnSelector = '#main-content > div > div > div.container > div > div > div.card.card--light-shadow.login-widget.col-md-6 > div.widget__body > div.login-form > form > div.align-end > span > input'
				automateLoginToSite(request, username, password, url, loginBtnSelector, 1)

			elif "Science Direct" in request.POST:
				global browser
				browser = Browser('chrome')
				try:
					browser.visit(url)
					browser.find_by_css("#bdd-email").fill(username)
					browser.find_by_css('#bdd-elsPrimaryBtn').click()
					browser.find_by_css("#bdd-password").fill(password)
					browser.find_by_css('#bdd-elsPrimaryBtn').click()
				except:
					messages.success(request,'Failed to access the database. Try Again Later.')

			elif "Directory of Open Access Books" in request.POST:
				automateLoginToSite(request, username, password, url, '', 2)

			elif "Zlibrary" in request.POST:
				automateLoginToSite(request, username, password, url, '', 2)

			return redirect("cifir:networklibraries_view")

class viewBook(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		collection = Collection.objects.filter(user=request.user)
		collection_book = Collection_book.objects.filter(user=request.user)

		context = {
				'collections' : collection,
				}
		return render(request, 'files.html', context)

	def post(self,request):
		
		if request.method == 'POST':
			if 'editCollectionBtn' in request.POST:
				print('clicked')
				collection_new_name = request.POST.get("name")
				collection_id = request.POST.get("id")
				print(collection_new_name)
				update_collection = Collection.objects.filter(id=collection_id).update(name=collection_new_name)
				print('save')

				messages.success(request,'Collection Edited Successfully!')
				return redirect('cifir:collections_view')

			elif 'deleteCollectionBtn' in request.POST:	

				print('Delete Button Clicked')
				collection_id = request.POST.get("id")
				collection = Collection.objects.filter(id = collection_id).update(isDeleted=True)
				print('Collection Deleted')

				messages.success(request,'Collection Deleted Successfully!')
				return redirect('cifir:collections_view')

		context = {}
		collection = request.POST.get('collection', None)
		collection_book = request.POST.get('collection_book', None)
		user = User.objects.filter(username=request.user)
		collection_name = Collection.objects.filter(user=request.user).filter(name=collection)
		collection_id = Collection.objects.filter(id=collection_name)
		# collection_book_id = Collection_book.filter(id=collection_book_id)
		book = Book.objects.filter(user=request.user)

		bookCollection = Collection.objects.get(id__in=collection_name)
		collectionBook = Collection.book.through.objects.filter(collection_id=bookCollection.id)

		context = {
					'collections' : collection,
					'collection_names' : collection_name,
					'collection_books' : collection_book,
					'books' : book,
					'collectionBook': collectionBook,
				}

		
		return render(request, 'files.html', context)


# #IMPORT USERS FROM CSV

# Current_Date = datetime.today().strftime ('%d-%b-%Y')
# User = get_user_model()
# loc1 = 'C:/accounts.csv'
# # loc2 = 'C:/accounts-saved'+str(Current_Date)+str(random.randint(0,100))+'.csv'
# # os.rename(loc1,loc2)
# file = loc1
# data = csv.reader(open(file,'r'), delimiter=",")


# for row in data:
#     if row[1] != "Number":
#         # Post.id = row[0]
#         Post=User()
#         usernameRow = row[3]
#         userUsername = User.objects.filter(username = usernameRow).values_list('username', flat=True).first()
#         print(userUsername)
#         if userUsername == row[3]:
#             print(userUsername)
#             userUsername = User.objects.filter(username = row[3]).values('username')[0]
#             finalUsername = userUsername['username']
#             print("User object: " + finalUsername)
#             print("Row data: " + usernameRow)
#             if finalUsername == usernameRow:
#                 print('data are equal')
#             # next(data)
#         else:
#         	Post.first_name = row[1]
#         	Post.last_name=row[2]
#         	Post.username = row[3]
#         	Post.email = row[4]
#         	Post.set_password(row[5])
# 	        # Post.last_login = "2018-09-27 05:51:42.521991"
# 	        Post.is_superuser = "0"
# 	        Post.is_staff = "1"
# 	        Post.is_active = "1"
# 	        # Post.date_joined = "2018-09-27 05:14:50"
# 	        print('data is saved')
# 	        Post.save()



# # #IMPORT USERS FROM CSV-end


#API
class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# class LoggedinUser(APIView):

#     def get(self, request):
#         user = get_user_model().objects.filter(id=request.user.id)
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data)


class BookList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # print(request.user)
        books = Book.objects.filter(user=request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetails(APIView):
    permission_classes = [AllowAny]

    def get_object(self, id):
        try:
            return Book.objects.get(id=id)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # print(request.user)
        collections = Collection.objects.filter(
            user=request.user).filter(isDeleted=False)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetails(APIView):
    permission_classes = [AllowAny]

    def get_object(self, id):
        try:
            return Collection.objects.get(id=id)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        collection = self.get_object(id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
