from django.urls import path
from users import views

app_name='user'
urlpatterns=[
    path('login/', views.LoginUser.as_view(), name='login'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('edit_profile/', views.EditUser.as_view(), name='edit'),
]