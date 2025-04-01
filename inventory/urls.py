from django.urls import path

from inventory import views

app_name='inventory'
urlpatterns=[
    path('', views.InventoryView.as_view(), name='inventory'),
]