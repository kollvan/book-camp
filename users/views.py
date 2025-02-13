from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title':'Авторизация',
    }

    def get_success_url(self):
        return reverse_lazy('main:index')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title':'Регистрация'
    }
    success_url = reverse_lazy('user:login')

def logout_user(request):
    logout(request)
    return redirect('main:index')

@login_required
def profile(request):
    return render(request, 'users/profile.html')