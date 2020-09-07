from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Product,CartItems,BillingAddress,NewsLetters
from .forms import BillingAddressForm


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
        good = super().get_object()
        context['goods'] = Product.objects.all().exclude(id = good.id)
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
            cart_item = CartItems(cart = cart,product = product,quantity = quantity)
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
            cart_count_lst = [int(key[10:]) for key in request.COOKIES.keys() if key.startswith('product_id')]
#            print(cart_count_lst)
            if cart_count_lst:
                print("I am in the cookie")
                data['cart_items'] = cart_count = len(cart_count_lst) + 1
                max_cart_count = max(cart_count_lst)
                response = JsonResponse(data)
                response.set_cookie(f"product_id{max_cart_count + 1}",product.id)
                response.set_cookie(f"product_name{max_cart_count + 1}",product.name)
                response.set_cookie(f"quantity{max_cart_count + 1}",quantity)
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
    template_name = 'app/cart.html'
    context_object_name = 'cart'
    
    def get_queryset(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return self.request.user.cart.cartitems_set.all()
        else:
            cart = []
            try:
#                cart_count = int(self.request.COOKIES.get('cart_count'))
                cart_count_lst = [int(key[10:]) for key in self.request.COOKIES.keys() if key.startswith('product_id')]
                print(cart_count_lst)
                for num in cart_count_lst:
                    cart_item = (
                        get_object_or_404(Product, id = int(self.request.COOKIES.get(f'product_id{num}'))),
                        self.request.COOKIES.get(f'quantity{num}'),
                        num
                    )
    #                print(cart_item)
                    cart.append(cart_item)
            except TypeError:
                pass
            return cart
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        important_info(self,context)
        # Remove some unwanted fields
        context.pop('object_list')
        context.pop('cart_items')
        print(context)
        return context

    
class IncreaseCartItemQuantityView(generic.View):
    """ This class decreases the quantity of an item in the user's cart"""
    
    def get(self,request,*args,**kwargs):
        cart_item_id = int(request.GET.get('cartItemId'));
        # User is signed in
        if request.user.is_authenticated:
            cart_item = get_object_or_404(request.user.cart.cartitems_set.all(),id = cart_item_id)
            cart_item.quantity += 1
            cart_item.save()
            return JsonResponse({})
        # User has not signed in
        else:
            response = JsonResponse({})
            # Increase the quantity in the cookie
            new_qty = int(request.COOKIES.get(f'quantity{cart_item_id}')) + 1
            response.set_cookie(f'quantity{cart_item_id}',new_qty)
            return response
            
    

class DecreaseCartItemQuantityView(generic.View):
    """ This class decreases the quantity of an item in the user's cart"""
    
    def get(self,request,*args,**kwargs):
        cart_item_id = int(request.GET.get('cartItemId'))
        # User has signed in
        if request.user.is_authenticated:
            cart_item = get_object_or_404(request.user.cart.cartitems_set.all(),id = cart_item_id)
            cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({})
        # Anonymous User
        else:
            response = JsonResponse({})
            # Decrease the quantity in the cookie
            new_qty = int(request.COOKIES.get(f'quantity{cart_item_id}')) - 1
            response.set_cookie(f'quantity{cart_item_id}',new_qty)
            return response
            

class DeleteCartItemView(generic.View):
    """ This class removes an item from the user's cart """
    
    def get(self,request,*args,**kwargs):
        cart_item_id= int(request.GET.get('cartItemId'))
        # Registered User
        if request.user.is_authenticated:
            cart_item = get_object_or_404(request.user.cart.cartitems_set.all(),id = cart_item_id)
            cart_item.delete()
            data = {
                'cart_items_count' : request.user.cart.cartitems_set.count()
            }
            return JsonResponse(data)
        # Unregistered User
        else:
            data = {
                'cart_items_count': int(request.COOKIES.get('cart_count')) - 1
            }
            response = JsonResponse(data)
            # Modify the cart count
            response.set_cookie('cart_count',data.get('cart_items_count'))
            print(dir(request.COOKIES))
            #Remove the item with that id
            response.delete_cookie(f'product_id{cart_item_id}')
            response.delete_cookie(f'product_name{cart_item_id}')
            response.delete_cookie(f'quantity{cart_item_id}')
            return response
            
class CheckoutView(generic.View):
    """ This class displays the billing address form """
    form_class = BillingAddressForm
    template_name = 'app/checkout.html'
    
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        try:
            billing = request.user.billingaddress
            form = self.form_class(instance = billing)
        except BillingAddress.DoesNotExist:
            initial = {
                'first_name':request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            }
            form = self.form_class(initial = initial)
        context = {
            'form':form
        }
        important_info(self,context)
        context['cart_items'] = request.user.cart.cartitems_set.all()
        return render(request,self.template_name,context)
    
    
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        try:
            billing = request.user.billingaddress
            form = self.form_class(request.POST,instance = billing)
            if form.is_valid() and form.changed_data:
                form.instance.user = request.user
                form.save()
                
        except BillingAddress.DoesNotExist:
            initial = {
                'first_name':request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            }
            form = self.form_class(request.POST,initial = initial)
            if form.is_valid and form.changed_data:
                form.instance.user = request.user
                form.save()
                
        context = {
            'form':form
        }
        important_info(self,context)
        context['cart_items'] = request.user.cart.cartitems_set.all()
        
        return render(request,self.template_name,context)
    

class SearchResultsView(generic.View):
    """ This class returns all matched items in the searchbar """
    
    def get(self,request,*args,**kwargs):
        q = request.GET.get('q')
        data = {
            'products': {product.name: product.id for product in  Product.objects.filter(name__icontains = q)[:5]}
        }
        data['results'] = True if data['products'] else False
#        print(data)
        return JsonResponse(data)

class NewsLettersView(generic.View):
    """ This class adds a new email to the news letters """
    
    def get(self,request,*args,**kwargs):
        email = request.GET.get('email')
        try:
            get_object_or_404(NewsLetters,email = email)
            print("This email is already in the database")
        except NewsLetters.DoesNotExist:
            news_letters = NewsLetters(email = email)
            news_letters.save()
            print("This email is not present")
        return JsonResponse({})
    
class OrdersView(generic.View):
    """ This shows all the orders the user has made """
    
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        return render(request,'app/orders.html')