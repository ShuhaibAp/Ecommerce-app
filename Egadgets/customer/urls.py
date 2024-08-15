from django.urls import path
from .views import *


urlpatterns=[
    path('chome',cHomeView.as_view(),name='chome'),
    path('plist/<str:cat>',ProductList.as_view(),name='plist'),
    path('pdet/<int:id>',ProductDetails.as_view(),name='pdet'),
    path('addc/<int:id>',AddCart,name='addc'),
    path('clist',CartList.as_view(),name='clist'),
    path('crem/<int:id>',RemoveCart,name='crem'),
    path('qinc/<int:id>',IncQuantity,name='qinc'),
    path('qdec/<int:id>',DecQuantity,name='qdec'),
    path('check/<int:id>',Checkout.as_view(),name='check'),
]