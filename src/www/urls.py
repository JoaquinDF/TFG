from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^adminsite', adminsite, name='adminsite'),
    url(r'^', index, name='index')
]
