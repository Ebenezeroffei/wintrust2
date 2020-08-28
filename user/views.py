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
from .forms import NewUser

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
            messages.success(request,f'You account has been succesfully created, you can sign in now.')
            return HttpResponseRedirect(reverse('user:signin'))
        return render(request,self.template_name,{'form':form})