from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=250)
	book_author = models.CharField(max_length=250)
	cover = models.ImageField(upload_to='media')
	file = models.FileField(upload_to='media')
	user = models.ManyToManyField(User, blank=True)
	isFavorite = models.BooleanField(default=False)
	isHaveRead = models.BooleanField(default=False)
	isToRead = models.BooleanField(default=False)
	isAddedToCol = models.BooleanField(default=False)
	isDeleted = models.BooleanField(default=False)

	class Meta:
		db_table = "Book"
		verbose_name_plural = "Books"

	def __str__(self):
		return self.title

class Collection(models.Model):
	name = models.CharField(max_length=250)
	book = models.ManyToManyField(Book, blank=True)
	user = models.ManyToManyField(User, blank=True)
	isDeleted = models.BooleanField(default=False)

	class Meta:
		db_table = "Collection"
		verbose_name_plural = "Collections"

	def __str__(self):
		return self.name

class Note(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name="notes_book")
	title = models.CharField(max_length=250)
	content = models.CharField(max_length=250)

	class Meta:
		db_table = "Note"
		verbose_name_plural = "Notes"

	def __str__(self):
		return self.title

class Catalog(models.Model):
	name = models.CharField(max_length=250)
	link = models.CharField(max_length=250)
	description = models.CharField(max_length=250)
	cover = models.CharField(max_length=250)
	defaultUsername = models.CharField(max_length=150)
	defaultPassword = models.CharField(max_length=100)
	count = models.IntegerField()

	class Meta:
		db_table = "Catalog"
		verbose_name_plural = "Catalogs"

	def __str__(self):
		return self.name

class Bookmark(models.Model):
	bookpage = models.CharField(max_length=250)
	book = models.ManyToManyField(Book, blank=True)
	page_index = models.CharField(max_length=250)
	
	is_removed = models.BooleanField(default=False)	

	class Meta:
		db_table = "Bookmark"
		verbose_name_plural = "Bookmarks"

	def __str__(self):
		bookTitle = self.book.all().first()
		return bookTitle.title

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'