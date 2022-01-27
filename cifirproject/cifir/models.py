from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=250)
	book_author = models.CharField(max_length=250)
	cover = models.ImageField(upload_to='media/')
	file = models.FileField(upload_to='media/')
	user = models.ManyToManyField(User, blank=True)
	isFavorite = models.BooleanField(default=False)
	isHaveRead = models.BooleanField(default=False)
	isToRead = models.BooleanField(default=False)

	isDeleted = models.BooleanField(default=False)

	class Meta:
		db_table = "Book"
		verbose_name_plural = "Books"


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

class Bookmark(models.Model):
	bookpage = models.CharField(max_length=250)
	book = models.ManyToManyField(Book, blank=True)
	page_index = models.CharField(max_length=250)
	
	is_removed = models.BooleanField(default=False)

	class Meta:
		db_table = "Bookmark"
		verbose_name_plural = "Bookmarks"
