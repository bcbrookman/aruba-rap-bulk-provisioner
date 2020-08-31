from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_index, name='index'),
    path('search', views.search_index, name='index'),
    path('about', views.search_about, name='about'),
]
