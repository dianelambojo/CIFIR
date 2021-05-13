from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Collection)
admin.site.register(Favorite)
admin.site.register(Note)
admin.site.register(Catalog)
admin.site.register(Library)