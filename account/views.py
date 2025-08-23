from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect
from django.views import View
from .forms import LoginForm,RegisterForm,AddressCreationForm
from .models import Register,User,Contact
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth import login, authenticate

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
                form.add_error('username','invalied phone')
        else:
            form.add_error('username','invalid data') 

        return render(request,'account/login.html',{'form':form})    
    

class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home:home')  # Replace 'home:home' with your URL name

    def form_valid(self, form):
        user = form.save()  # Save the new user
        # Authenticate the user
        authenticated_user = authenticate(
            phone=user.phone,
            password=form.cleaned_data['password1']  # or the appropriate password field
        )
        if authenticated_user is not None:
            login(self.request, authenticated_user)  # Log the user in
        return super().form_valid(form)


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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')  
        Contact.objects.create(fullname=name , email=email , description = message)
        return redirect('/') 
    return render(request,'account/contact-us.html')

def profile(request):
    return render(request,'account/profile.html',{})








