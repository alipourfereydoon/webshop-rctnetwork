from django.shortcuts import render
from django.views.generic import DetailView,TemplateView,ListView
from product.models import Product,Category


class ProductDetailView(DetailView):
    model = Product
    template_name='product/product_detail.html'


class NavbarPartialView(TemplateView):
    template_name = 'includes/navbar.html'
    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView , self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

# class ProductsListView(ListView):
#     template_name='product/products_list.html'
#     queryset = Product.objects.all()
#     context_object_name = 'products'

#     def get_context_data(self, **kwargs):
#         request = self.request
#         colors = request.GET.getlist('color')
#         sizes = request.GET.getlist('size')
#         min_price = int(request.GET.get('min_price'))
#         max_price = int(request.GET.get('max_price'))
#         queryset = Product.objects.all()
#         if colors:
#             queryset = queryset.filter(color__title__in=colors).distinct()
#         if sizes:
#             queryset = queryset.filter(size__title__in= sizes).distinct() 
#         if min_price and max_price:
#             queryset = queryset.filter(price__lte= max_price , price__gte =min_price)       
#         context = super(ProductsListView , self).get_context_data()
#         context['object_list'] = queryset
#         return context


class ProductsListView(ListView):
    template_name='product/products_list.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        # Get filter parameters
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Filter by colors if provided
        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()

        # Filter by sizes if provided
        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        # Filter by price range if provided
        try:
            if min_price:
                min_price_value = float(min_price)
                queryset = queryset.filter(price__gte=min_price_value)
            if max_price:
                max_price_value = float(max_price)
                queryset = queryset.filter(price__lte=max_price_value)
        except ValueError:
            # Handle invalid input gracefully, e.g., ignore filter or set default
            pass

        return queryset