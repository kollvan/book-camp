from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileForm
from users.messages import MessageResponse


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Вход в акаунт',
    }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(request, MessageResponse.INCORRECT_PASSWORD_OR_LOGIN)
            return self.form_invalid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация'
    }
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        messages.success(self.request, MessageResponse.USER_SUCCESS_CREATE)
        return super().form_valid(form)



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
        'title': 'Редактировать профиль',
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user:profile')


class ExtendPasswordResetDoneView(PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        messages.info(request, MessageResponse.PASSWORD_RESET_DONE)
        return redirect('main:index')


class ExtendPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, MessageResponse.PASSWORD_RESET_COMPLETE)
        return redirect('user:login')
