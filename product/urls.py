from django.urls import path
from .import views

app_name = 'Product'
urlpatterns = [
    path('<int:pk>',views.ProductDetailView.as_view(), name='product_detail'),
    path('navbar',views.NavbarPartialView.as_view(),name='navbar'),
    path('all',views.ProductsListView.as_view(),name='products_list')
]
