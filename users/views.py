from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from users.forms import UserForm, UserRegisterForm, UserForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only



# Create your views here.
class LoginView(View):
    template_name = 'users/login.html'
    form_class = UserForm
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('books:home')
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form})
    def post(self, request):
        form =self.form_class(request.POST)
        user = authenticate(username =request.POST['username'],password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('books:home')
            form=self.form_class(None)
            return render(request, self.template_name,{'form':form})
        else:
            messages.error(request, f'Wrong username or password')
            return redirect('login')
        
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context ={
        'u_form':u_form,
        'p_form':p_form,
    }
    
    return render(request,'users/profile.html',context)


def view_404(request, exception):
    return render(request,'users/404.html')

def view_500(request):
    return render(request,'users/500.html')

