from django.urls import path
from  estoapp import views
from  django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [


    path('', views.index,name ='index'),
    path('admin_page',views.admin_page,name="admin_page"),
    path('category_page',views.category_page,name='category_page'),
    
]