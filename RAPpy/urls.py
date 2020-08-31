from django.urls import path

from . import views

urlpatterns = [
    path('', views.RAPpy_index, name='index'),
    path('search', views.RAPpy_index, name='index'),
    path('about', views.RAPpy_about, name='about'),
]
