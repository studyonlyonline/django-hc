"""harbacore_home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'parent_module'

urlpatterns = [
    path('index/', views.Index.as_view(), name="index_page"),
    path('contact-form/', views.contact_form_view, name="contact_form"),
    path('home/', include('home_module.urls', namespace='home_module')),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()