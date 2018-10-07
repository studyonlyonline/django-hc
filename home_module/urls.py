from django.urls import path

from . import views

app_name = 'home_module'

urlpatterns = [
    path('', views.index, name='index'),
    path('schemes/', views.schemes_list, name="schemes_default_page"),
    path('schemes/<int:scheme_id>', views.schemes_list, name="schemes_detail_page"),
    path('category/', views.product_list, name="product_default_page"),
    path('category/<int:category_id>', views.product_list, name="product_list_page"),
]