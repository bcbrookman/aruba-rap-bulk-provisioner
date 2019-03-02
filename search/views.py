from django.shortcuts import render
from django.http import JsonResponse
from . api_search import api_search as search


def search_index(request):
    return render(request, 'search/search.html')


def search_about(request):
    return render(request, "search/about.html")


def api_search(request, query):
    q = str(query)
    return JsonResponse(search(q))
