from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    # path('list/',views.ProductList,name='product_listhome'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('jobdetail1/<int:id>',views.jobdetail)
]
