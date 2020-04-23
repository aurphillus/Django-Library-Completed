from django import forms
from books.models import Upload, TBR, Book
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField

class FileUpload(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['name','file']
        
        
        
        


class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.title)

class TBRForm(forms.ModelForm):
    book = Book.objects.all()
    class Meta:
        model = TBR
        fields = ['title','book']
        
        widgets = {"book":CheckboxSelectMultiple(),}