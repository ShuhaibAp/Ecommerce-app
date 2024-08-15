from accounts.models import *

def cart_count(request):
    pcount=Cart.objects.filter(user=request.user).count()
    return {"cart_count":pcount}