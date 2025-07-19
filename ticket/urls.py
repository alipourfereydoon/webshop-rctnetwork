from django.urls import path
from . import views


app_name='ticket'
urlpatterns = [
    path('add',views.add_ticket, name='ticket')
]
