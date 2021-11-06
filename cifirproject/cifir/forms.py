from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from cifir.models import Book


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class BookForm(forms.ModelForm):
	class Meta:
 		model = Book
 		fields = ['file']

class PasswordChangingForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	class Meta:
 		model = User
 		fields = ['old_password','new_password1','new_password2']