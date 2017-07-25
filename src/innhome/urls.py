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

import extract
import transform
import linkage
import www

url_api_v1 = [
    url(r'^extract/', include(extract.urls, namespace='extract')),
    url(r'^transform/', include(transform.urls, namespace='transform')),
    url(r'^linkage/', include(linkage.urls, namespace='linkage')),
]

urlpatterns = [
    url(r'^www/', include(www.urls, namespace='www')),
    url(r'^api/v1/', include(url_api_v1, namespace='api')),
    url(r'^admin/', admin.site.urls),
]
