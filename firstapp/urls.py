from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contactus/', views.contactus2, name='contactus'),
    path('contactusclass/', views.ContactUs.as_view(), name='contactclass'),
]
