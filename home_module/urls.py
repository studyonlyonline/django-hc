from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schemes', views.schemes_list, name="schemes_page"),
]