from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from webshop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('account/',include('account.urls')),
    path('products/',include('product.urls')),
    path('cart/',include('cart.urls')),
    path('ticket/',include('ticket.urls')),

]

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
