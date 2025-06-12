from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }
    #Может пригодиться
    # def form_invalid(self, form):
    #     messages.success(
    #         self.request,
    #         '''Проверьте свою почту, мы отправили Вам ссылку,
    #         которую можно использовать для входа на сайт.''')
    #     return super().form_invalid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация'
    }
    success_url = reverse_lazy('user:login')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('main:index')


class ProfileUser(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Bookcamp Profile - {self.request.user.username}'
        return context

class EditUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'
    extra_context = {
        'title':'Редактировать профиль',
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user:profile')
