from django.shortcuts import render
from django.views import generic
from .models import Product

# Create your views here.
class IndexView(generic.ListView):
    model = Product
    template_name = 'app/index.html'
    context_object_name = 'goods'
    
class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'good'
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['goods'] = Product.objects.all()
        return context
