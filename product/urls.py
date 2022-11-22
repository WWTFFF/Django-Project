from django.urls import path

from . import views

urlpatterns = [
    path('recommend', views.get_recommended_products, name='get_recommended_products')
]
