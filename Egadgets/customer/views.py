from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,TemplateView,ListView,DetailView,DeleteView
from accounts.models import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail

#decorator
def login_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.warning(request,"Login required")
            return redirect('log')

dec=[login_required,never_cache]

# Create your views here.
# @method_decorator(decorator=dec,name='dispatch')
class cHomeView(TemplateView):
    template_name="cHome.html"

@method_decorator(decorator=dec,name='dispatch')
class ProductList(ListView):
    template_name="productlist.html"
    queryset=Product.objects.all()
    context_object_name="products"
    def get_queryset(self):
        qset=super().get_queryset().filter(category=self.kwargs.get('cat'))
        return qset

@method_decorator(decorator=dec,name='dispatch')
class ProductDetails(DetailView):
    template_name="productdet.html"
    queryset=Product.objects.all()
    context_object_name='product'
    pk_url_kwarg='id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        reviews = Review.objects.filter(product=product)
        context['review'] = reviews
        return context

dec
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

@method_decorator(decorator=dec,name='dispatch')
class CartList(ListView):
    template_name='cartlist.html'
    queryset=Cart.objects.all()
    context_object_name='cart'
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

dec
def RemoveCart(request,*args,**kwargs):
    cid=kwargs.get('id')
    cart=Cart.objects.get(id=cid).delete()
    messages.success(request,"Item removed from cart!")
    return redirect('clist')

dec    
def IncQuantity(request,**kwargs):
    qid=kwargs.get('id')
    quant=Cart.objects.get(id=qid)
    quant.quantity+=1
    quant.save()
    return redirect('clist')

dec
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

dec
def mailsending(cart,request):
    try:
        sub="Egadgets - Order Placed"
        msg=f"You'r order for {cart.product.title} with rupees {cart.product.price} has been placed"
        from_mail="faketanjiro1@gmailcom"
        to_mail=[request.user.email]
        send_mail(sub,msg,from_mail,to_mail)
    except:
        print("Mail sending failed...")

@method_decorator(decorator=dec,name='dispatch')
class Checkout(DetailView):
    template_name="checkout.html"
    queryset=Cart.objects.all()
    pk_url_kwarg='id'
    context_object_name="item"
    def post(self,request,*args,**kwargs):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        pid=kwargs.get('id')
        cart=Cart.objects.get(id=pid)
        product=cart.product
        quantity=cart.quantity
        user=request.user
        Orders.objects.create(product=product,user=user,quantity=quantity,address=address,phone=phone)
        mailsending(cart,request)
        cart.delete()
        messages.success(request,"Order placed!")
        return redirect('clist')

@method_decorator(decorator=dec,name='dispatch')
class OrderList(ListView):
    template_name='orderList.html'
    queryset=Orders.objects.all()
    context_object_name='order'
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

@method_decorator(decorator=dec,name='dispatch')
class DeleteOrder(View):
    def get(self,request,**kwargs):
        pid=kwargs.get('id')
        product=Orders.objects.get(id=pid).delete()
        return redirect('order')

dec
def AddReview(request,**kwargs):
    pid=kwargs.get('id')
    prod=Product.objects.get(id=pid)
    user=request.user
    rev=request.POST.get('review')
    rev=Review.objects.create(review=rev, user=user, product=prod)
    return redirect('pdet', id=pid)

# class Reviews(DetailView):
#     template_name="productdet.html"
#     queryset=Review.objects.all()
#     context_object_name='review'
#     pk_url_kwarg='id'    
