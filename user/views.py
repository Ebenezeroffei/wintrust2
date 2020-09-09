# IMPORTS
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views import View,generic
from app.models import Cart,NewsLetters,Orders
from .forms import NewUser,EditUserProfileForm
from app.views import important_info

# Create your views here.

class LoginUserView(LoginView):
    """ This class is reponsible for signin up users """
    template_name = 'user/forms_login.html'
    
    def get_success_url(self,*args,**kwargs):
        return reverse('app:home')

class SignUpUser(View):
    form_class = NewUser
    template_name = 'user/forms_signup.html'
    
    def get(self,request,*args,**kwargs):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username = form.cleaned_data.get('username'))
            # Create the cart for the user
            cart = Cart(user = user)
            cart.save()
            # Create the user's orders
            order = Orders(user = user)
            order.save()
            # Add the user's email to the news letters
            try:
                get_object_or_404(NewsLetters,email = form.cleaned_data.get('email'))
            except NewsLetters.DoesNotExist:
                news_letters = NewsLetters(email = form.cleaned_data.get('username'))
                news_letters.save()
            messages.success(request,f'You account has been succesfully created, you can sign in now.')
            return HttpResponseRedirect(reverse('user:signin'))
        return render(request,self.template_name,{'form':form})
    
class UserProfileView(generic.View):
    """ This class shows the profile of the user """
    form_class = EditUserProfileForm
    template_name= 'user/profile.html'
    
    @method_decorator(login_required(login_url = '/signin/' ))
    def get(self,request,*args,**kwargs):
        form = self.form_class(instance = request.user)
        context = {
            'form': form
        }
        important_info(self,context)
        return render(request,self.template_name,context)
    
    
    
    @method_decorator(login_required(login_url = '/sigin/' ))
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,instance = request.user)
        if form.is_valid and form.changed_data:
            print('I have been changed')
            print(form.changed_data)
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            print('I have not been changed')
        
        context = {
            'form': form
        }
        important_info(self,context)
        return render(request,self.template_name,context)
    