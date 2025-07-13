from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from product.models import Product

class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        self.request.session.get('my_name','ali')    
        return context
    
class ProductList(ListView):
    model = Product.objects.all()
    context_object_name = 'products'
    template_name='home/index.html'


def aboutus(request):
    return render(request,'home/aboutus.html',{})
    