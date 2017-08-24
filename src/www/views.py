from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', context={'title': 'Innhome'})


def indexsearch(request):
    return render(request, 'index-search.html', context={'title': 'Search'})
