from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    title=models.CharField(max_length=30)
    desc=models.CharField(max_length=100)
    price=models.IntegerField()
    options=(
        ("SmartPhone","SmartPhone"),
        ("SmartWatch","SmartWatch"),
        ("Tablets","Tablets"),
        ("Laptops","Laptops"),
    )
    category=models.CharField(max_length=30,choices=options,default="SmartPhone")
    image=models.ImageField(upload_to="product_images",null=True)
    wish=models.ManyToManyField(User,blank=True)
    def __str__(self):
        return self.title




class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    quantity=models.IntegerField(default=1)
    @property
    def total_amount(self):
        return self.product.price * self.quantity

class Orders(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    quantity=models.IntegerField()
    address=models.CharField(max_length=100)
    phone=models.IntegerField()
    options=(
        ("Order Placed","Order Placed"),
        ("Order Shipped","Order Shipped"),
        ("Out for delivery","Out for delivery"),
        ("Order Delivered","Order Delivered"),
    )
    status=models.CharField(max_length=50,default="Order Placed",choices=options)
    @property
    def total_amount(self):
        return self.product.price * self.quantity