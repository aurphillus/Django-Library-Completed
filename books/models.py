from django.db import models
from django.db.models.signals import pre_save
from books.utils import unique_slug_generator, unique_slug_generator_author, unique_slug_generator_genre
from django.urls import reverse
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from books.validators import validate_file_extension


# Create your models here.


# Book Manager
class BookManager(models.Manager):
    def is_read(self):
        return self.filter(read='y')
    
    def is_not_read(self):
        return self.filter(read='n')
    
    def name(self):
        return self.first_name
    
    

# Author 
class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Enter first name of the author")
    last_name = models.CharField(max_length=100, help_text="Enter last name of the author",blank="true")
    slug = models.SlugField(max_length=250, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        return reverse('books:authordetail',kwargs={'id': self.slug})
    
    class Meta:
        unique_together = ("first_name", "last_name")
        

# Genre
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    slug = models.SlugField(max_length=250, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:genredetail',kwargs={'id': self.slug})



# Book
class Book(models.Model):
    
    YES = 'y'
    NO = 'n'
    
    DID_READ_CHOICES = [
        (YES,'Yes'),
        (NO,'No'),
    ]
        
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    author = models.ManyToManyField(
        Author,
        related_name='author_books',
        blank=False,
        )
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book',related_name='genre_books', blank=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book',blank=True,null=True)
    read = models.CharField(
        max_length=1,
        choices=DID_READ_CHOICES,
        default=NO,
        )
    cover = models.ImageField(default='uploads/cover/default.png',upload_to="uploads/cover/",blank=True,null=True)
    image_url = models.URLField(blank=True)
    extension = models.CharField(max_length=100,blank=True)
    file = models.FileField(upload_to="uploads/file/",blank=True,null=True, validators=[validate_file_extension])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    objects = BookManager()
    
    class Meta:
        ordering = ['title']
        
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:bookdetail',kwargs={'id': self.slug})
    
    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.file.delete()
        super().delete(*args, **kwargs)
    
    
# TBR
class TBR(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    book = models.ManyToManyField(
        Book,
        related_name='in_tbr',
        blank=False,
        default="uncategorised"
        )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:tbrdetail',kwargs={'id': self.slug})

def get_remote_image(sender,instance, *args, **kwargs):
    if instance.image_url and not instance.cover:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(instance.image_url).read())
        img_temp.flush()
        instance.cover.save(f"image_{instance.pk}", File(img_temp))

def slug_generator_genre(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_genre(instance)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def slug_generator_author(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_author(instance)


def file_type(sender,instance,*args, **kwargs):
    if instance.file:
        ext = instance.file.name.split('.')[-1]
        instance.extension = ext
            

def file_name_change(sender, instance, *args, **kwargs):
    if instance.file:
        ext = instance.file.name.split('.')[-1]
        instance.file.name =  '{}.{}'.format(instance.slug,ext)

pre_save.connect(slug_generator,sender=TBR)
pre_save.connect(slug_generator,sender=Book)
pre_save.connect(slug_generator_author,sender=Author)
pre_save.connect(slug_generator_genre,sender=Genre)
pre_save.connect(file_name_change,sender=Book)
pre_save.connect(get_remote_image,sender=Book)
pre_save.connect(file_type,sender=Book)








class Upload(models.Model):
    name=models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="uploads/processing/")
    


