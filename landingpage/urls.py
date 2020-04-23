from django.urls import path
from landingpage.views import *



urlpatterns = [
    path('',landingpage,name="landingpage"),
]
