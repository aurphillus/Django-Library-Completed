from django.shortcuts import render
from landingpage.models import Quote

# Create your views here.

def landingpage(request):
    context ={
        'object': Quote.objects.random(),
    }
    return render(request,'landingpage/index.html',context)