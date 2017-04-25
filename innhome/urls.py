"""
innhome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from etl.views import BotViewSet, CrawlerViewSet, DataViewSet

router = routers.DefaultRouter()
router.register(r'bot', BotViewSet, r'bot')
router.register(r'crawler', CrawlerViewSet, r'crawler')
router.register(r'data', DataViewSet, r'dada')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls, namespace='api.tutorial')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
