import django_filters
from books.models import Book

class BookFilter(django_filters.FilterSet):
    
    class Meta:
        model = Book
        fields = {
            'title':['icontains'],
            }