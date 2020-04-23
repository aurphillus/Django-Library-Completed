from django.contrib import admin
from books.models import Genre, Author, Book, TBR

# Register your models here.

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(TBR)