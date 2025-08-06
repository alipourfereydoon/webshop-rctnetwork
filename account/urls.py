from django.urls import path
from . import views

app_name='account'
urlpatterns = [
    path('login',views.UserLogin.as_view(), name='user_login'),
    path('register',views.RegisterView.as_view(),name='user_register'),
    path('logout',views.userlogout,name='user_logout'),
    path('add/address',views.AddAddressView.as_view(),name='add_address'),
    path('contact-us',views.contactus,name='contact-us')

]
