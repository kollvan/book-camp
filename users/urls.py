from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from users import views
from users.views import ExtendPasswordResetDoneView

app_name='user'
urlpatterns=[
    path('login/', views.LoginUser.as_view(), name='login'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('edit_profile/', views.EditUser.as_view(), name='edit'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('user:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', ExtendPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('user:password_reset_complete'),
        ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]