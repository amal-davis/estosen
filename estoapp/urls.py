from django.urls import path
from  estoapp import views
from  django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [


    path('', views.index,name ='index'),
    path('admin_page',views.admin_page,name="admin_page"),
    path('category_page',views.category_page,name='category_page'),
    path('categories/<str:category_name>/',views.categories, name='categories'),
    path('productpage/',views.productpage,name='productpage'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('p_editpage/<int:pk>/',views.p_editpage,name='p_editpage'),
    path('p_edit_form/<int:pk>',views.p_edit_form,name="p_edit_form"),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('p_delete_form/<int:pk>',views.p_delete_form,name='p_delete_form'),



    
]