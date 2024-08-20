from django.urls import path
from .views import *

urlpatterns=[
    path("Elog",ELogin.as_view(),name='Elog'),
    path("Elout",Elogout,name='Elout'),
    path("Ereg",ERegister.as_view(),name='Ereg'),
]