from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.views import View,generic
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test
from app.models import Product

# Create your views here.
    
class AdminSigninView(View):
    """ This class allows the admininstrator to signin """
    template_name = 'control/admin_signin.html'
    
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {}
        try:
            user = authenticate(username = username,password = password)
            if user.is_superuser:
                login(request,user)
                return HttpResponseRedirect(reverse('control:admin_home'))
            else:
                context['error'] = 'You are not an admin.'
        except AttributeError:
            context['error'] = 'Invalid credentilals. Try Again.'
        return render(request,self.template_name,context)


    
class LogoutAdminView(View):
    """ This class logouts an admin """
    
    def dispatch(self,request,*args,**kwargs):
        logout(request)
        return redirect('control:admin_signin')
    
class AdminHomeView(UserPassesTestMixin,LoginRequiredMixin,generic.ListView):
    """ This class is responsible for displaying the landing page for the admin """
    model = Product
    template_name = 'control/index.html'
    context_object_name = 'goods'
    
    def test_func(self,*args,**kwargs):
        return self.request.user.is_superuser
    
    def get_login_url(self,*args,**kwargs):
        return reverse('control:admin_signin')
        
        
class AdminAddProductView(UserPassesTestMixin,LoginRequiredMixin,generic.CreateView):
    """ This allows the admin to add a new product """
    model = Product
    fields = ['name','price','image1','image2','image3','description']
    template_name = 'control/product_form.html'
    
    def test_func(self,*args,**kwargs):
        return self.request.user.is_superuser
    
    def get_login_url(self,*args,**kwargs):
        return reverse('control:admin_signin')
    
class AdminProductDetailView(UserPassesTestMixin,LoginRequiredMixin,generic.DetailView):
    """ This class displays the details of a product """
    model = Product
    context_object_name = 'good'
    template_name = 'control/products_detail.html'
    
    def test_func(self,*args,**kwargs):
        return self.request.user.is_superuser
    
    def get_login_url(self,*args,**kwargs):
        return reverse('control:signin')
    
    
class AdminUpdateProductView(UserPassesTestMixin,LoginRequiredMixin,generic.UpdateView):
    """ This allows the admin to add a new product """
    model = Product
    fields = ['name','price','image1','image2','image3','description']
    template_name = 'control/product_form.html'
    context_object_name = 'good'
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['update'] = True
        return context
    
    def test_func(self,*args,**kwargs):
        return self.request.user.is_superuser
    
    def get_login_url(self,*args,**kwargs):
        return reverse('control:admin_signin')
    
        
class AdminRemoveProductView(View):
    """ This view removes a product """
    
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    @method_decorator(login_required(login_url = "/admin/"))
    def get(self,request,*args,**kwargs):
        product_id = int(request.GET.get('productId'))
        product = get_object_or_404(Product,id = product_id)
        product.delete()
        data = {
            'product_id': product_id
        }
    
        return JsonResponse(data)