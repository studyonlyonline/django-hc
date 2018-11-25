from django.urls import path

from . import views

app_name = 'home_module'

urlpatterns = [
    path('', views.index, name='index'),
    path('schemes/', views.SchemesListView.as_view(), name="schemes_default_page"),
    path('schemes/<int:scheme_id>', views.SchemesListView.as_view(), name="schemes_detail_page"),
    path('category/', views.ProductListView.as_view(), name="product_default_page"),
    path('category/<int:category_id>', views.ProductListView.as_view(), name="product_list_page"),
    path('test/<int:name>', views.TestListView.as_view(), name="test_list_page"),
    path('cartAdd/', views.AddToCartSessionView.as_view(), name='add_to_cart_session'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('updateCartQuantity/<str:id>/<int:quantity>', views.UpdateCartQuantity.as_view(), name="update_cart_quantity"),
    path('submitOrder/', views.SubmitOrderView.as_view(), name="submit_order")
]