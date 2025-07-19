from django.shortcuts import render,redirect
from . models import Ticket


def add_ticket(request):
    title = request.GET.get('name')
    body = request.GET.get('body')
    if title and body:
        Ticket.objects.create(title=title , body=body)
        return redirect('/')
        
    return render(request,'ticket/addticket.html')