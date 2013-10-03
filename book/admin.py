# coding=utf-8

from django.contrib import admin
from book.models import Publisher, Author, Book

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)