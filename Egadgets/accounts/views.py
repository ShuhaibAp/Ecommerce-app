from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,CreateView
from .forms import *
from django.contrib.auth import authenticate,login
from django.contrib import messages
# Create your views here.

class Ehome(TemplateView):
    template_name="index.html"

class ELogin(FormView):
    template_name="loginNew.html"
    form_class=ELoginForm
    def post(self,request):
        form_data=ELoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            login(request,user)
            if user:
                # messages.success(request,"Login Successfull!")
                return redirect('chome')
            else:
                messages.error(request,"Invalid Username or Password")
                return render(request,"loginNew.html",{'form':form_data})
        return render(request,"loginNew.html",{'form':form_data})


class ERegister(CreateView):
    template_name="reg.html"
    form_class=ERegForm
    success_url=reverse_lazy('Elog')