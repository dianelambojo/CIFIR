from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=250)
	cover = models.ImageField(upload_to='media/')
	file = models.FileField(upload_to='media/')
	user = models.ManyToManyField(User, blank=True)
	isFavorite = models.BooleanField(default=False)
	isHaveRead = models.BooleanField(default=False)
	isToRead = models.BooleanField(default=False)

	class Meta:
		db_table = "Book"
		verbose_name_plural = "Books"

class Author(models.Model):
	firstname = models.CharField(max_length=250)
	lastname = models.CharField(max_length=250)
	book = models.ManyToManyField(Book, blank=True)

	class Meta:
		db_table = "Author"
		verbose_name_plural = "Authors"

class Collection(models.Model):
	name = models.CharField(max_length=250)
	book = models.ManyToManyField(Book, blank=True)
	user = models.ManyToManyField(User, blank=True)
	isDeleted = models.BooleanField(default=False)

	class Meta:
		db_table = "Collection"
		verbose_name_plural = "Collections"

class Note(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name="notes_book")
	title = models.CharField(max_length=250)
	content = models.CharField(max_length=250)

	class Meta:
		db_table = "Note"
		verbose_name_plural = "Notes"

class Catalog(models.Model):
	name = models.CharField(max_length=250)
	link = models.CharField(max_length=250)
	description = models.CharField(max_length=250)
	cover = models.CharField(max_length=250)
	defaultUsername = models.CharField(max_length=150)
	defaultPassword = models.CharField(max_length=100)

	class Meta:
		db_table = "Catalog"
		verbose_name_plural = "Catalogs"

class LibUser(models.Model):
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	password = models.CharField(max_length=200, default ='')
	#password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		db_table = "LibUser"
		verbose_name_plural = "LibUsers" 
