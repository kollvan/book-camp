from django.urls import path

from inventory import views

app_name='inventory'
urlpatterns=[
    path('collection/', views.InventoryView.as_view(), name='collection'),
    path('widgets/user_data/<slug:product_slug>/', views.UserDataView.as_view(), name='widget_user_data'),
    path('widgets/reviews/<slug:product_slug>/', views.ProductReviewsView.as_view(), name='widget_reviews')
]