from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100','placeholder':"password"}))
    username = forms.EmailField(widget=forms.TextInput(attrs={'class':'input100','placeholder':"username or email"}))
    
    class Meta:
        model = User
        fields =['username','password']
        

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username','class': 'input100'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'email','class': 'input100'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password','class': 'input100'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password','class': 'input100'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']