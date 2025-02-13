from django.urls import path
from users import views

app_name='user'
urlpatterns=[
    path('login/', views.LoginUser.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register')
]