from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class indexView(View):
	def get(self, request):
		return render(request,'index.html')

class homePageView(View):
	def get(self, request):
		return render(request,'base.html')