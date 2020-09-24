from django.contrib import admin

# Register your models here.

from .models import Library, Book, Clip

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Clip)
