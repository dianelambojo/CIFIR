from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class indexView(View):
	def get(self, request):
		return render(request,'index.html')

class homePageView(View):
	def get(self, request):
		return render(request,'homepage.html')

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