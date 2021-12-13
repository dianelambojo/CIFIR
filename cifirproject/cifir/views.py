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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.decorators import method_decorator
import zipfile
from lxml import etree
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 
import time
import undetected_chromedriver as chromedriver
import csv, sys, os, django, random, datetime
from pathlib import Path
import PyPDF2
from PyPDF2 import PdfFileReader
import pyttsx3
import fitz
import pdfplumber
from ebooklib import epub
import ebooklib
import os
import nltk

chromedriver.TARGET_VERSION = 96
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
	print('book added')

def setDriverOptions():
	options = webdriver.ChromeOptions()
	options.add_experimental_option("detach", True)

	return options

def automateLogin(username, password, url, loginBtnSelector, indicator):
	driver = webdriver.Chrome(executable_path=r'C:/Program Files/Google/Chrome/Application/chromedriver.exe', options=setDriverOptions())
	if indicator == 1:
		driver.get(url)
		username_field = driver.find_element_by_css_selector("#username")
		username_field.send_keys(username)
		driver.execute_script("document.querySelector('#password').setAttribute('value','"+ password +"')")
		driver.execute_script("document.querySelector('"+ loginBtnSelector +"').click();")
	
	if indicator == 2:
		driver.get(url)

def tts(book_id):
	# pdf = "C:/Users/HP/Documents/Project Trials/TrialTexttoSpeech/textTospeech/TTS/BehindHerEyes.pdf"
	# pdfFileObject = open(r'C:\Users\HP\Documents\Project Trials\TrialTexttoSpeech\textTospeech\TTS\\BehindHerEyes.pdf', 'rb')
	books = Book.objects.filter(id=book_id)
	print(book_id)
	
	print('tts activated')
	print(book_id)
	book = Book.objects.get(book_id)
	pdf = pdfplumber.open(book)
	page = pdf.pages[1]
	text = page.extract_text()
	# input_path = r"C:/"
	# german_corpus = []
	# book = epub.read_epub(os.path.join(input_path,'1541217285_wuthering-heights_g7Cc0CH.epub'))
	# for doc in book.get_items():
	# 	doc_content = str(doc.content)
 #    	for w in nltk.word_tokenize(doc_content):
 #    		german_corpus.append(w.lower())

	print(text)

	speak = pyttsx3.init('sapi5')
	voices = speak.getProperty('voices')
	speak.setProperty("rate", 178)
	speak.setProperty("voice", voices[0].id)

	speak.say(text)
	speak.runAndWait()

	return text
	# pdf.close()


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
			ext = os.path.splitext(file.name)[1]  # [0] returns path+filename
			epub_extensions = ['.epub']
			pdf_extensions = ['.pdf']
			if ext.lower() in epub_extensions:
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

				return redirect('cifir:home_view')

			if ext.lower() in pdf_extensions:
				#pdf file format
				book = Book.objects.create(title= file.name, file = file)
				book.user.add(user)
				messages.success(request,'Book added!')

				return redirect('cifir:home_view')

		if 'updateBookStatus' in request.POST:
			updateBookStatus(request.POST.get('item'), request.POST.get('book_id'))
			messages.success(request,"Book updated!")
			return redirect('cifir:home_view')
		if 'addToCollection' in request.POST:
			print('hi there')
			addToCollection(request.POST.get('book_id'), request.POST.get('collection_id'))
			return redirect('cifir:home_view')
		if 'removeFromCollection' in request.POST:
			# insert code here
			print("insert code here to remove from collection")

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
						if user.check_password(123456):
							messages.info(request, "Please reset your password in Account Setting.")
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

class adminPageView(View):
	def get(self, request):
		return render(request,'admin/base_site.html')

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

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
        account_activation_token = TokenGenerator()

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":'imcastbound@gmail.com',
					'domain':'127.0.0.1:8000',
					'site_name': 'CIFIR',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , ['imcastbound@gmail.com'], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset_form.html", context={"password_reset_form":password_reset_form})


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
		if request.method == "POST":
			book_id = request.POST.get('book_id', None)
			user = User.objects.filter(username=request.user)
			book = Book.objects.filter(user=request.user).filter(id=book_id)

			context = {
						'books' : book,
					}
			print(book_id)
			if 'click-me' in request.POST:
				print('read request')
				print(book)
				# tts(book_id)
				messages.success(request,"Text To Speech Starting...")
				return render(request, 'EpubRead.html', context)

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
		context = {}
		book_id = request.POST.get('book_id', None)
		user = User.objects.filter(username=request.user)
		book = Book.objects.filter(user=request.user).filter(id=book_id)

		context = {
					'books' : book,
				}

		if 'click-me' in request.POST:
			print('read request')
			# tts(book_id)

			# return HttpResponse(tts())

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
		collection_book = Collection_book.objects.filter(user=request.user)

		context = {
				'collections' : collection,
				}
		return render(request, 'files.html', context)

	def post(self,request):
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
# loc2 = 'C:/accounts-saved'+str(Current_Date)+str(random.randint(0,100))+'.csv'
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


