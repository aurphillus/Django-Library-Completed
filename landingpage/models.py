from django.db import models
from random import randint
from django.db.models import Count

# Create your models here.
class QuoteManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

class Quote(models.Model):
    quote = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    
    objects = QuoteManager()
    
    def __str__(self):
        return f"{self.author}'s Quote"