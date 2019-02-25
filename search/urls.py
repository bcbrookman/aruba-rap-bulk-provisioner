from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.index, name='index'),
    path('about', views.about, name='about'),
    path('api/search/<query>', views.api_search, name='search')
]
