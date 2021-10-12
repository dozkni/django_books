from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from store.models import Book

# Register your models here.
#admin.site.register(Book)

@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass