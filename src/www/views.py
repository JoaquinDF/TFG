from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', context={'title': 'Innhome'})


def adminsite(request):
    return render(request, 'admin-site.template.html', context={'title': 'Admin'})
