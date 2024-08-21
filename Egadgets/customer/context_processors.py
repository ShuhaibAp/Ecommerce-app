from accounts.models import *

def cart_count(request):
    if request.user.is_authenticated:
        pcount=Cart.objects.filter(user=request.user).count()
        return {"cart_count":pcount}
    return {"cart_count":0}