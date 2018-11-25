from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('profile/', views.CreateProfile.as_view(), name='create_profile'),
    path('dealer/', views.DealerDetails.as_view(), name='dealer_details'),

]