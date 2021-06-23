from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from cifir.models import LibUser
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Collection)
admin.site.register(Note)
admin.site.register(Catalog)

@admin.register(LibUser)
class UserAdmin(ImportExportModelAdmin):
	list_display = ("firstname","lastname", "email", "password")
	pass