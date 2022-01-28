from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(Book)
admin.site.register(Collection)
admin.site.register(Note)
admin.site.register(Catalog)
admin.site.register(Bookmark)


class UserAdmin(ImportExportModelAdmin):
	list_display = ("firstname","lastname", "email", "password")
	pass