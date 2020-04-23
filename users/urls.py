from django.urls import path
from users.views import *
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/',LoginView.as_view(),name="login"),
    path('profile/',profile,name="profile"),
    path('register/',register,name="register"),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    

    
]
