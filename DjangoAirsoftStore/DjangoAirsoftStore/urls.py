"""DjangoAirsoftStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, URLPattern, re_path
from rest_framework import routers

from store.views import BlastersViewSet, oauth, UserBlasterRelationView

router = routers.SimpleRouter()

router.register(r'blasters', BlastersViewSet)
router.register(r'blaster_relation', UserBlasterRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')), #namespace нужен, чтобы работал реверс
    path('auth/', oauth),
    path('__debug__/', include('debug_toolbar.urls')),
]
urlpatterns += router.urls




