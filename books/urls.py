from django.contrib import admin
from django.urls import path ,include
from books.views import *


app_name = 'books'

urlpatterns = [
    path('', home,name='home'),
    
    # Author
    
    path('author/',AuthorListView.as_view(),name='authorlist'),
    path('author/add/',AuthorCreateView.as_view(),name="authoradd"),
    path('author/<slug:id>/update/',AuthorUpdateView.as_view(),name="authorupdate"),
    path('author/<slug:id>/delete/',AuthorDeleteView.as_view(),name="authordelete"), 
    path('author/<slug:id>/',AuthorDetail,name="authordetail"),
    
    
    # Book
    path('book/',BooksListView.as_view(),name='booklist'),
    path('book/add/',BookCreateView.as_view(),name='bookcreate'),
    path('book/<slug:id>/delete/',BookDeleteView.as_view(),name="bookdelete"),
    path('book/<slug:id>/update/',BookUpdateView.as_view(),name="bookupdate"),
    path('book/<slug:id>/',BooksDetailView.as_view(),name="bookdetail"),
    
    # TBR
    path('readinglist/',TBRListView.as_view(),name='tbrlist'),
    path('readinglist/add/',TBRCreate.as_view(),name='tbrcreate'),
    path('readinglist/<slug:id>/update/',TBRUpdate.as_view(),name='tbrupdate'),
    path('readinglist/<slug:id>/delete/',TBRDelete.as_view(),name='tbrdelete'),
    path('readinglist/<slug:id>/',TBRDetail,name='tbrdetail'),
    
    # Genre
    path('genre/',GenreListView.as_view(),name="genrelist"),
    path('genre/add/',GenreCreateView.as_view(),name="genrecreate"),
    path('genre/<slug:id>/update/',GenreUpdateView.as_view(),name="genreupdate"),
    path('genre/<slug:id>/delete/',GenreDeleteView.as_view(),name="genredelete"),
    path('genre/<slug:id>/',GenreDetail,name="genredetail"),

    # Batch Process
    path('batchupload/',batchprocess,name="batchload"),
    
    #Search
    path('search/',Search.as_view(),name="search"),
    
    ]
