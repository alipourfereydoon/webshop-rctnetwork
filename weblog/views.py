from django.shortcuts import render


def blog(request):
    return render(request,'weblog/design.html',{})
