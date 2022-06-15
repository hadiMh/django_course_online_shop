from django.urls import path

from .views import order_create_view

urlpatterns = [
    path('create/', order_create_view, name='order_create'),
]
