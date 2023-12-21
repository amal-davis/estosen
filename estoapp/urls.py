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
    path('product_search/', views.product_search, name='product_search'),
    path('signup_page',views.signup_page,name='signup_page'),
    path('login_page',views.login_page,name='login_page'),
    path('usercreate',views.usercreate,name='usercreate'),
    path('signin',views.signin,name='signin'),
    path('cart',views.cart,name='cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('logout',views.logout,name='logout'),
    path('UserDetails',views.UserDetails,name='UserDetails'),
    path('ad_userdelete/<int:pk>',views.ad_userdelete,name='ad_userdelete'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('review_details',views.review_details,name='review_details'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('allproducts',views.allproducts,name='allproducts'),
    path('add_to_cart_details/<int:pk>/', views.add_to_cart_details, name='add_to_cart_details'),


    
]