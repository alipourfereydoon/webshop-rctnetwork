from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from product.models import Product
from .cart_madule import Cart
from . models import Order,OrderItem,DiscountCode
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from account.models import Address


class CartDetailView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request,'cart/cart_detail.html',{'cart':cart})
    

class CartAddView(View):
    def post(self,request,pk):
        product = get_object_or_404(Product,id=pk)
        color,size,quantity=request.POST.get('color'),request.POST.get('size'),request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product,quantity,color,size)
        return redirect('cart:cart_detail')
    
class CartDeleteView(View):
    def get(self,request,id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')    
    

class OrderDetailView(View):
    def get(self , request , pk):
        order = get_object_or_404(Order,id=pk)
        return render(request,'cart/order_detail.html',{'order':order})


class OrderCreationView(View):
    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user , total_price = cart.total())
        for item in cart:
            OrderItem.objects.create(order=order,product = item['product'],color=item['color'],size=item['size'], quantity = item['quantity'], price = item['price'])
        cart.remove_cart()
        return redirect('cart:order_detail', order.id) 
    
class ApplyDiscountView(View):
    def post(self,request,pk):
        order = get_object_or_404(Order,id=pk)
        code = request.POST.get('discount_code')  
        discount_code= get_object_or_404(DiscountCode,name=code)
        if discount_code.quantity == 0:
            return redirect('cart:order_detail',order.id)
        order.total_price -= order.total_price * discount_code.discount / 100
        order.save()
        discount_code.quantity -=1
        discount_code.save()
        return redirect('cart:order_detail',order.id)





MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'ali.pourferydoon1983@gmail.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/cart/verify/' # Important: need to edit for realy server.


# Important: need to edit for realy server.


class SendRequestView(View):
    def post(self , request , pk):
        order = get_object_or_404(Order, id=pk , user=request.user)
        address = get_object_or_404(Address,id=request.POST.get('address'))
        order.address = f'{address.address}-{address.phone}'
        order.save()
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.total_price,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone }
        }
        req_header = {"accept": "application/json",
                    "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")



