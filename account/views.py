from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect,reverse
from django.views import View
from .forms import LoginForm,OtpLoginForm,CheckOtpForm,AddressCreationForm
import ghasedakpack
from random import randint
from .models import Otp,User,Contact
from django.utils.crypto import get_random_string
from uuid import uuid4

SMS=ghasedakpack.Ghasedak('b4f8d77dfd2aaea9275d9a113c4825e0452893ae36ed3333797dea152c32d805LSZeryMyLPnu2SQ5')


class UserLogin(View):
    def get(self,request):
        form = LoginForm()
        return render(request,'account/login.html',{'form':form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request,user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')
            else:
                form.add_error('phone','invalied phone')
        else:
            form.add_error('phone','invalid data') 

        return render(request,'account/login.html',{'form':form})    
    
class OtpLoginView(View):
    def get(self,request):
        form = OtpLoginForm()
        return render(request,'account/otp_login.html',{'form':form})

    def post(self,request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000,9999)
            SMS.verification({'receptor':cd["phone"],'type':'1', 'template':'Ghasedak','param1':randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'],code=randcode,token=token)
            print(randcode)
            return redirect(reverse('account:check_otp')+ f'?token={token}')
        else:
            form.add_error("phone",'invalide data')
        return render(request,'account/otp_login.html',{'form':form})   


class CheckOtpView(View):
        def get(self,request):
            form = CheckOtpForm()
            return render(request,'account/check_otp.html',{'form':form})

        def post(self,request):
            token = request.GET.get('token')
            form = CheckOtpForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if Otp.objects.filter(code=cd["phone"],token=token).exists():
                    otp = Otp.objects.get(token=token)
                    user, is_create = User.objects.get_or_create(phone=otp.phone)
                    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    otp.delete()
                    return redirect('/')
                
            else:
                form.add_error("phone",'invalide data')
            return render(request,'account/check_otp.html',{'form':form})  

class AddAddressView(View):
    def post(self,request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page=request.GET.get('next')
            if next_page:
                return redirect(next_page)

        return render(request,'account/add_address.html',{'form':form})

    def get(self,request):
        form = AddressCreationForm()
        return render(request,'account/add_address.html',{'form':form})    


def userlogout(request):
    logout(request)
    return redirect('/')

def contactus(request):
    name = request.GET.get('name')
    email = request.GET.get('email')
    message = request.GET.get('message')
    if name and email and message:
        Contact.objects.create(fullname=name , email=email , description = message)
        return redirect('/')
    return render(request,'account/contact-us.html')








