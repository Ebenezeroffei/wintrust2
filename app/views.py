from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views import generic
from .models import Product,CartItems



def important_info(inst,context):
    # Number of items in the users cart
    context['cart_items_count'] = inst.request.user.cart.cartitems_set.count() if inst.request.user.is_authenticated else inst.request.COOKIES.get('cart_count') if inst.request.COOKIES.get('cart_count') else 0
    # All items in the cart
    context['cart_items'] = [item.product.name for item in inst.request.user.cart.cartitems_set.all()] if inst.request.user.is_authenticated else [value for key,value in inst.request.COOKIES.items() if key.startswith('product_name')]

# Create your views here.
class IndexView(generic.ListView):
    model = Product
    template_name = 'app/index.html'
    context_object_name = 'goods'
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        important_info(self,context)
#        print(context)
        return context
    
class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'good'
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['goods'] = Product.objects.all()
        important_info(self,context)
        return context
    
class AddItemToCartView(generic.View):
    """ This class adds an item to the users cart """
    def get(self,request,*args,**kwargs):
        product_id = int(request.GET.get('productId'))
        quantity = int(request.GET.get('quantity'))
        product = get_object_or_404(Product,id = product_id)
        # User has signed in
        if request.user.is_authenticated:
            print("I have signed in")
            cart = request.user.cart
            cart_item = CartItems(cart = cart,product = product)
            cart_item.save() # Save the itme to the user's cart
            data = {
                'cart_items': cart.cartitems_set.count()
            }
            return JsonResponse(data)
        # No user has signed in
        else:
            print("I have not signed in")
            data = {}
#            response = JsonResponse(data)
            if request.COOKIES.get('cart_count'):
                print("I am in the cookie")
                data['cart_items'] = cart_count = int(request.COOKIES.get('cart_count')) + 1
                response = JsonResponse(data)
                response.set_cookie(f"product_id{cart_count}",product.id)
                response.set_cookie(f"product_name{cart_count}",product.name)
                response.set_cookie(f"quantity{cart_count}",quantity)
                response.set_cookie(f"cart_count",cart_count)
            else:
                print("I am not in the cookie")
                data['cart_items'] = 1
                response = JsonResponse(data)
                response.set_cookie('cart_count',1)
                response.set_cookie(f"product_id1",product.id)
                response.set_cookie(f"product_name1",product.name)
                response.set_cookie(f"quantity1",quantity)
#            request.COOKIES = {}
#            print([value for key,value in request.COOKIES.items() if key.startswith('product_name')])
            return response

class CartView(generic.ListView):
    model = Product
    template_name = 'app/cart.html'
    
    def get_queryset(self,*args,**kwargs):
        return self.request.user.cart.cartitems_set.all()
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        important_info(self,context)
        print(context)
        return context
