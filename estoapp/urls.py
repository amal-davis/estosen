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
    path('checkout_page',views.checkout_page,name='checkout_page'),
    path('checkout_view',views.checkout_view,name='checkout_view'),
    path('confirmation_page',views.confirmation_page,name='confirmation_page'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('model_registration',views.model_registration,name='model_registration'),
    path('model_dashboard',views.model_dashboard,name='model_dashboard'),
    path('modelcreate',views.modelcreate,name='modelcreate'),
    path('model_edit/<int:pk>/',views.model_edit,name='model_edit'),
    path('update_password',views.update_password,name='update_password'),
    path('model_details',views.model_details,name='model_details'),
    path('approve_model/<int:model_id>/', views.approve_model, name='approve_model'),
    path('disapprove_model/<int:model_id>/', views.disapprove_model, name='disapprove_model'),
    path('save_image_to_another_database/', views.save_image_to_another_database, name='save_image_to_another_database'),
    path('another_database_model_details/<int:model_id>/', views.another_database_model_details, name='another_database_model_details'),
    path('delete_model/<int:model_id>/', views.delete_model_view, name='delete_model'),
    path('model_image_control',views.model_image_control,name='model_image_control'),
    path('delete_model_profile/<int:pk>/', views.delete_model_profile, name='delete_model_profile'),
    path('add_blog',views.add_blog,name='add_blog'),
    path('save_blog_section',views.save_blog_section,name='save_blog_section'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('confirm_product',views.confirm_product,name='confirm_product'),
    path('payment_confirmation_page',views.payment_confirmation_page,name='payment_confirmation_page'),
    path('order_admin',views.order_admin,name='order_admin'),
    path('order_page',views.order_page,name='order_page'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('web_image_section',views.web_image_section,name='web_image_section'),
    path('slider_content_add',views.slider_content_add,name='slider_content_add'),
    path('save_slider_content',views.save_slider_content,name='save_slider_content'),
    path('delete_slider_content/<int:content_id>/', views.delete_slider_content, name='delete_slider_content'),
    path('edit_slider_content/<int:content_id>/', views.edit_slider_content, name='edit_slider_content'),
    path('fashion_section',views.fashion_section,name='fashion_section'),
    path('add_fashion_section/<int:section_id>/', views.add_fashion_section, name='add_fashion_section'),
    path('delete_fashion_entry/<int:section_id>/<int:entry_id>/', views.delete_fashion_entry, name='delete_fashion_entry'),
    path('edit_fashion_entry/<int:section_id>/<int:entry_id>/', views.edit_fashion_entry, name='edit_fashion_entry'),
    path('fashion_check_section',views.fashion_check_section,name='fashion_check_section'),
    path('edit_fashion_content/<int:content_id>/', views.edit_fashion_content, name='edit_fashion_content'),
    path('delete_fashion_content/<int:content_id>/', views.delete_fashion_content, name='delete_fashion_content'),







    
]