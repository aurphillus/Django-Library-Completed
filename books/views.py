from django.shortcuts import render
from django.shortcuts import redirect, render
from books.models import Genre, Author, Book, TBR
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from books.forms import FileUpload
import pandas as pd
from books.author_slug import unique_slug_generator_author
from books.book_slug import unique_slug_generator
import json
import logging
from django.utils.text import slugify
import numpy as np
from django.contrib.auth.decorators import login_required
from books.filters import BookFilter
from books.forms import TBRForm

# Create your views here.


# Search

class Search(ListView):
    model = Book
    template_name = 'books/search.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        return context


# Dashboard Home

def home(request):
    context = {
        'books' : Book.objects.all().count(),
        'authors': Author.objects.all().count(),
        'genres': Genre.objects.all().count(),
        'tbrs': TBR.objects.all().count(),
        'latest': Book.objects.all().order_by('-created_on')[:7],
        'tbr_list': TBR.objects.all().order_by('-created_on')[:7],
    }
    return render(request,'books/dashboard.html',context)

#############################################################################

# Author

class AuthorListView(ListView):
    model = Author
    ordering = ['first_name']
    paginate_by = 10
    

def AuthorDetail(request,id):
    context = {
        'author': Author.objects.get(slug=id),
        'author_books': Author.objects.get(slug=id).author_books.all(),
        'books_count': Author.objects.get(slug=id).author_books.all().count(),
    }
    return render(request,'books/author_detail.html',context)

class AuthorCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Author
    fields = ['first_name','last_name']
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
  
class AuthorUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Author
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    fields = ['first_name','last_name']
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
    
class AuthorDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('books:authorlist')
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
        


###########################################################################

# Book

class BooksListView(ListView):
    model = Book 
    ordering = ['title']
    
    paginate_by = 10
        # <app>/<model>_<viewtype>.html
    
class BooksDetailView(DetailView):
    model = Book
    slug_field = 'slug'
    slug_url_kwarg = 'id'

class BookCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Book
    fields = ['title','author','genre','summary','read','cover','file']
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
    
class BookUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Book
    fields = ['title','author','genre','summary','read','cover','file']
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
    
class BookDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books:booklist')
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False


###############################################################################

# TBR

class TBRListView(ListView):
    paginate_by = 10
    model = TBR
    
def TBRDetail(request, id):
    context = {
        'tbr' : TBR.objects.get(slug=id),
        'books': TBR.objects.get(slug=id).book.all(),
    }
    return render(request,'books/tbr_detail.html',context)

class TBRCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = TBR
    form_class = TBRForm
    
    fields = ['title','book']

    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
    

class TBRUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = TBR
    fields = ['title','book']
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
    
class TBRDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = TBR
    success_url = reverse_lazy('books:tbrlist')
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
        
#################################################################################

# Genre

class GenreListView(ListView):
    model = Genre
    paginate_by = 10
    

def GenreDetail(request,id):
    context = {
        'genre': Genre.objects.get(slug=id),
        'genre_books': Genre.objects.get(slug=id).genre_books.all(),
        'genre_count': Genre.objects.get(slug=id).genre_books.all().count(),
    }
    return render(request,'books/genre_detail.html',context)

class GenreCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Genre
    fields = ['name']
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

class GenreUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Genre
    fields = ['name']
    slug_field = 'slug'
    slug_url_kwarg = 'id'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
    
class GenreDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Genre
    success_url = reverse_lazy('books:genrelist')
    slug_field = 'slug'
    slug_url_kwarg = 'id'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False
        


#########################################################################################

# File Loading
def remove(string): 
    return string.replace(", ", ",")

def isNaN(num):
    return num != num

def run(inp_list=None,tbr_name=None):
    
    cont = []
    log = []
    new_author = 0
    new_book = 0
    new_genres = 0
    new_tbr = 0
    records_json = json.loads(inp_list)
    
    if tbr_name:
        tbr_slug = unique_slug_generator(tbr_name)
        try:
            tbr = TBR.objects.get(slug=tbr_slug)
            return None
        except TBR.DoesNotExist:
            log.append("Creating a new TBR:  {}".format(tbr_name))
            tbr = TBR(title=tbr_name)
            tbr.save()
            new_tbr=+1
            tbr = TBR.objects.get(slug=tbr_slug)

            for record in records_json:
                auth_name_refined = remove(record['author_name'])
                auth_name = auth_name_refined.split(",")
                
                # Loading Authors to the database, if doesn't exist. Creating one
                for ind_auth_name in auth_name:
                    firstname = ind_auth_name.strip().split(' ')[0]
                    lastname = ' '.join((ind_auth_name + ' ').split(' ')[1:]).strip()
                    auth_slug = unique_slug_generator_author(ind_auth_name)
                    try:
                        author = Author.objects.get(slug=auth_slug)
                        log.append("Auhtor: {},{} exists.".format(lastname,firstname))
                    
                    except Author.DoesNotExist:
                        log.append("Author: {} {} does not exist.".format(lastname,firstname))
                        author = Author(first_name=firstname,last_name=lastname)
                        author.save()
                        new_author=+1
                        log.append("Author: {} {} Added.".format(lastname,firstname))
                        
                
                #Loading Books to the database. if doesn't exist. Creating one
                try:
                    book = Book.objects.get(slug=record["book_slug"])
                    for auth in auth_name:
                        auth_slug = unique_slug_generator_author(auth)
                        log.append("Book: {} Exists.".format(record["book_title"]))
                        author = Author.objects.get(slug=auth_slug)
                        book.author.add(author)
                        book.save()
                        log.append("Added Author to Book: {}.".format(record["book_title"]))
                        tbr.book.add(book)
                        tbr.save()
                        log.append("Added Book to Reading List: {}.".format(tbr_name))
                
                except Book.DoesNotExist:
                    log.append("Book: {} does not exist.".format(record["book_title"]))
                    book = Book(title=record["book_title"],image_url=record["image_url"])
                    book.save()
                    new_book+=1
                    log.append("Book: {} Added.".format(record["book_title"]))
                    book = Book.objects.get(slug=record["book_slug"])
                    for auth in auth_name:
                        auth_slug = unique_slug_generator_author(auth)
                        author = Author.objects.get(slug=auth_slug)
                        book.author.add(author)
                        book.save()
                        log.append("Added Author to Book: {}.".format(record["book_title"]))
                        tbr.book.add(book)
                        tbr.save()
                        log.append("Added Book to Reading List: {}.".format(tbr_name))
                        
                
                # Loading Genre to the database. if doesn't exist. Creating One
                if record['genre']:
                    genre_refined = remove(record['genre'])
                    genre_name = genre_refined.split(",")
                    
                    for genre in genre_name:
                        genre_slug = unique_slug_generator(genre)
                        try:
                            gen = Genre.objects.get(slug=genre_slug)
                            log.append("Genre: {} Exists.".format(genre))
                            
                        except Genre.DoesNotExist:
                            log.append("Genre: {} does not exist.".format(genre))
                            gen = Genre(name=genre)
                            gen.save()
                            new_genres+=1
                            log.append("Genre: {} added.".format(genre))
                            
                # Adding Genres to the books
                try:
                    book = Book.objects.get(slug=record["book_slug"])
                    for genre in genre_name:
                        genre_slug = unique_slug_generator_author(genre)
                        log.append("Book: {} Exists.".format(record["book_title"]))
                        genre = Genre.objects.get(slug=genre_slug)
                        book.genre.add(genre)
                        book.save()
                        log.append("Added Genre{} to Book: {}.".format(genre,record["book_title"]))
                
                except Exception as e:
                    pass
                
    else:
        for record in records_json:
            auth_name_refined = remove(record['author_name'])
            auth_name = auth_name_refined.split(",")
            
            # Loading Authors to the database, if doesn't exist. Creating one
            for ind_auth_name in auth_name:
                firstname = ind_auth_name.strip().split(' ')[0]
                lastname = ' '.join((ind_auth_name + ' ').split(' ')[1:]).strip()
                auth_slug = unique_slug_generator_author(ind_auth_name)
                try:
                    author = Author.objects.get(slug=auth_slug)
                    log.append("Auhtor: {},{} exists.".format(lastname,firstname))
                
                except Author.DoesNotExist:
                    log.append("Author: {} {} does not exist.".format(lastname,firstname))
                    author = Author(first_name=firstname,last_name=lastname)
                    author.save()
                    new_author+=1
                    log.append("Author: {} {} Added.".format(lastname,firstname))
                    
            
            #Loading Books to the database. if doesn't exist. Creating one
            try:
                book = Book.objects.get(slug=record["book_slug"])
                for auth in auth_name:
                    auth_slug = unique_slug_generator_author(auth)
                    log.append("Book: {} Exists.".format(record["book_title"]))
                    author = Author.objects.get(slug=auth_slug)
                    book.author.add(author)
                    book.save()
                    log.append("Added Author to Book: {}.".format(record["book_title"]))

            
            except Book.DoesNotExist:
                log.append("Book: {} does not exist.".format(record["book_title"]))
                
                # book = Book(title=record["book_title"])
                book = Book(title=record["book_title"],image_url=record["image_url"])
                book.save()
                new_book+=1
                log.append("Book: {} Added.".format(record["book_title"]))
                book = Book.objects.get(slug=record["book_slug"])
                for auth in auth_name:
                    auth_slug = unique_slug_generator_author(auth)
                    author = Author.objects.get(slug=auth_slug)
                    book.author.add(author)
                    book.save()
                    log.append("Added Author to Book: {}.".format(record["book_title"]))

                    
            
            # Loading Genre to the database. if doesn't exist. Creating One
            if record['genre']:
                genre_refined = remove(record['genre'])
                genre_name = genre_refined.split(",")
                
                for genre in genre_name:
                    genre_slug = unique_slug_generator(genre)
                    try:
                        gen = Genre.objects.get(slug=genre_slug)
                        log.append("Genre: {} Exists.".format(genre))
                        
                    except Genre.DoesNotExist:
                        log.append("Genre: {} does not exist.".format(genre))
                        gen = Genre(name=genre)
                        gen.save()
                        new_genres=+1
                        log.append("Genre: {} added.".format(genre))
                        
            # Adding Genres to the books
            try:
                book = Book.objects.get(slug=record["book_slug"])
                for genre in genre_name:
                    genre_slug = unique_slug_generator_author(genre)
                    log.append("Book: {} Exists.".format(record["book_title"]))
                    genre = Genre.objects.get(slug=genre_slug)
                    book.genre.add(genre)
                    book.save()
                    log.append("Added Genre{} to Book: {}.".format(genre,record["book_title"]))
            
            except Exception as e:
                pass
    
    cont.append(new_author)
    cont.append(new_book)
    cont.append(new_genres)
    cont.append(new_tbr)
    cont.append(log)
    
    return cont
        
        
@login_required(login_url='login')
def batchprocess(request):
    form = FileUpload()
    
    context = {
        'form':form,
    }
    
    if request.method == "GET":
        return render(request,'books/batch_loading.html',context)
    
    try:
        try:
            name = request.POST["name"]
        except Exception as e:
            name= None
            
        file = request.FILES["file"]
        
        if not file.name.endswith('.xlsx'):
            messages.error(request,'File is not xlsx type')
            return HttpResponseRedirect(reverse("loading"))
        
        #if file is too large, return
        if file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("loading"))

        try:
            tbr = pd.read_excel(file)
            
            record = tbr[['book_title','author','genre','image_url']]
            record["genre"] = record["genre"].replace(np.nan, 'uncategorized', regex=True)
            record["image_url"] = record["image_url"].replace(np.nan, '', regex=True)
            
            record = record.dropna()
            
            records_list = record.values.tolist()
            cleaned_books_list = [x for x in records_list if str(x) != 'nan']
            books = []

            for records in cleaned_books_list:
                title = records[0]
                book_slug = unique_slug_generator(records[0])
                        
                books.append({
                    'book_title': title,
                    'book_slug': book_slug,
                    'author_name': records[1],
                    'genre':records[2],
                    'image_url':records[3],
                })
                
            book_json =[]
            book_json = json.dumps(books,indent=4)
            print(book_json)
                
            try:
                
                data = run(book_json,name)
                
                context={
                    'author':data[0],
                    'book':data[1],
                    'genre':data[2],
                    'tbr':data[3],
                    'log':data[4]
                }
                
                if data:
                    return render(request,'books/loading_success.html',context)
                else:
                    messages.error(request,"Processing file failed. Same Name TBR List exists ")
                    return render(request,'books/batch_loading.html')
                    
            except Exception as e:
                messages.error(request,"Processing file failed. "+repr(e))
                return render(request,'books/batch_loading.html')
    
        except Exception as e:
            messages.error(request,"Unable to upload file. "+repr(e))
            return render(request,'books/batch_loading.html')
            
        
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
  
    return render(request,'books/batch_loading.html')


