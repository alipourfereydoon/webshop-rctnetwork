from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from product.models import Product,Job

# class Home(TemplateView):
#     template_name = "home/index.html"

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)

#         self.request.session.get('my_name','ali')    
#         return context
    



class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve all products
        products = Product.objects.all()
        jobs=Job.objects.all()
        # Add products to context
        self.request.session.get('my_name','ali')  
        context['products'] = products
        context['jobs'] = jobs
        return context    
    # ---------------------------------------------------------------------------
# class ProductList(ListView):
#     model = Product.objects.all()
#     context_object_name = 'products'
#     template_name='home/index.html'

# def ProductList(request):
#     product = Product.objects.all()
#     return render(request,'home/index.html',context={'products':product}) 
# -----------------------------------------------------------------------------------
def aboutus(request):
    return render(request,'home/aboutus.html',{})
    
   