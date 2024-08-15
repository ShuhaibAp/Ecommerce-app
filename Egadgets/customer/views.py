from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView,ListView,DetailView
from accounts.models import *
from django.contrib import messages
# Create your views here.
class cHomeView(TemplateView):
    template_name="cHome.html"

class ProductList(ListView):
    template_name="productlist.html"
    queryset=Product.objects.all()
    context_object_name="products"
    def get_queryset(self):
        qset=super().get_queryset().filter(category=self.kwargs.get('cat'))
        return qset

class ProductDetails(DetailView):
    template_name="productdet.html"
    queryset=Product.objects.all()
    context_object_name='product'
    pk_url_kwarg='id'

def AddCart(request,*args,**kwargs):
    pid=kwargs.get('id')
    prod=Product.objects.get(id=pid)
    user=request.user
    quant=request.POST.get('qty')
    try:
        cart=Cart.objects.get(product=prod,user=user)
        cart.quantity+=int(quant)
        cart.save()
        messages.success(request,"Item Quantitiy Updated!")
        return redirect('chome')
    except:
        Cart.objects.create(product=prod,user=user,quantity=quant)
        messages.success(request,"Item added to cart!")
        return redirect('chome')

class CartList(ListView):
    template_name='cartlist.html'
    queryset=Cart.objects.all()
    context_object_name='cart'
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

def RemoveCart(request,*args,**kwargs):
    cid=kwargs.get('id')
    cart=Cart.objects.get(id=cid).delete()
    messages.success(request,"Item removed from cart!")
    return redirect('clist')
    
def IncQuantity(request,**kwargs):
    qid=kwargs.get('id')
    quant=Cart.objects.get(id=qid)
    quant.quantity+=1
    quant.save()
    return redirect('clist')

def DecQuantity(request,**kwargs):
    qid=kwargs.get('id')
    quant=Cart.objects.get(id=qid)
    if quant.quantity == 1:
        quant.delete()
        return redirect('clist')
    else:
        quant.quantity-=1
        quant.save()
    return redirect('clist')

class Checkout(DetailView):
    template_name="checkout.html"
    queryset=Cart.objects.all()
    pk_url_kwarg='id'
    context_object_name="item"
