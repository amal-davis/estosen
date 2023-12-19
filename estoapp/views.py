import select
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Avg




from .models import *
import random
import string
# Create your views here.


def index(request):
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    return render(request,'index.html',{'cart_quantity': total_quantity,'categories':categories,'carts': carts,})


def admin_page(request):
    return render(request,'admin.html')


def category_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        images = request.FILES.get('image')
        data = Category(name=name,image=images)
        data.save()
        return redirect('category_page')
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')

        category.name = name

        if image:
            category.image = image

        category.save()
        return redirect('category_page')

    categories = Category.objects.all()
    return render(request, 'category_edit.html', {'category': category, 'categories': categories})


def delete_category(request, category_id):
    category_to_delete = get_object_or_404(Category, pk=category_id)
    category_to_delete.delete()
    return redirect('category_page')


def categories(request, category_name):
    categories = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    context = {'category_name': category_name, 'cart_quantity': total_quantity, 'products': products,'categories':categories}
    return render(request, 'category_page.html', context)


def productpage(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        select = request.POST['select']
        quantity = request.POST['quantity']

        try:
            quantity = int(quantity)
        except ValueError:
            # Handle the case where quantity is not a valid integer
            # Set a default value for quantity or raise an error, depending on your requirements
            quantity = 0

        category = Category.objects.get(id=select)

        # Create the product
        product = Product(name=name, category=category, description=description, price=price, quantity=quantity)
        product.save()

        # Handle multiple file uploads
        for file in request.FILES.getlist('file'):
            image = Image_section(image=file)
            image.save()
            product.images.add(image)

        # Set status to 'Out of stock' if quantity is explicitly set to 0
        if product.quantity == 0:
            product.status = 'Out of stock'
        else:
            # Update status based on quantity
            if product.quantity < 5:
                product.status = 'Limited stock'
            else:
                product.status = 'In stock'

        product.save()

        return redirect('productpage')

    categories = Category.objects.all()
    product_detail = Product.objects.all()
    return render(request, 'ad_product.html', {'categories': categories, 'product': product_detail})


def p_delete_form(request,pk):
    edit=Product.objects.get(id=pk)
    edit.delete()
    return redirect('productpage')


def p_editpage(request,pk):
    edit = Product.objects.get(id=pk)
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request,'product_edit.html',{'product':edit},context)


def p_edit_form(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        product.name = request.POST.get('name')
        product.description = request.POST.get('description', '')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')

        # Update category
        select = request.POST.get('select')
        category = Category.objects.get(id=select)
        product.category = category

        # Update images
        old_images = list(product.images.all())
        new_images = request.FILES.getlist('file')

        if old_images and not new_images:
            # Keep the existing images
            product.images.set(old_images)
        elif new_images:
            # Update the images
            new_image_objects = [Image_section.objects.create(image=image) for image in new_images]
            product.images.set(new_image_objects)

        # Update status based on quantity
        try:
            quantity_int = int(product.quantity)
            if quantity_int == 0:
                product.status = 'Out of stock'
            elif 0 < quantity_int <= 5:
                product.status = 'Limited stock'
            else:
                product.status = 'In stock'
        except ValueError:
            # Handle the case where quantity is not a valid integer
            product.status = 'Unknown'

        product.save()
        return redirect('admin_page')

    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, 'product_edit.html', {'product': product, 'categories': categories})


def product_search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        products = Product.objects.filter(Q(name__icontains=search) | Q(category__name__icontains=search))
        return render(request, 'category_page.html', {'products': products})
    else:
        return render(request, 'category_page.html')


def signup_page(request):
    
    categories = Category.objects.all()
    return render(request,'signup.html',{'categories':categories})


def login_page(request):
    
    categories = Category.objects.all()
    return render(request,'login.html',{'categories':categories})


def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['fname']  
        last_name=request.POST['sname']  
        username=request.POST['uname']  
        password=request.POST['password']  
        cpassword=request.POST['cpassword']
        email=request.POST['email']
        phone_no=request.POST['phone_no']  


        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This user name already exists!')
                return redirect('signup_page')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()
                user_profile = UserProfile.objects.create(
                user=user,
                phone_number=phone_no)
                user_profile.save()
                print('Succeed....')
        else:
            messages.info(request,'Password doesnt match!!!!!')
            print('Password is not matching')
            return redirect('signup_page')
        return redirect('login_page')
    else:
        return render(request,'signup.html')
    

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_page')
            else:
                login(request,user)
                auth.login(request,user)
                # return redirect('')
                return redirect('index')
        else:
            return redirect('login_page')
    return redirect('login_page')





@login_required(login_url='signin')
def cart(request):
    carts = Cart.objects.filter(user=request.user)
    categories = Category.objects.all()
    total_price = 0
    total_quantity = carts.aggregate(Sum('quantity'))['quantity__sum'] or 0
    grand_total = sum(cart.product.price * cart.quantity for cart in carts)

    for cart in carts:
        subtotal = cart.product.price * cart.quantity
        total_price += subtotal
        cart.subtotal = subtotal
        # total_quantity += cart.quantity


    return render(request, 'cart.html', {'carts': carts, 'subtotal':subtotal, 'total_price': total_price, 'grand_total': grand_total, 'categories': categories, 'cart_quantity': total_quantity})
    

@login_required(login_url='signin')
def add_to_cart(request, pk):
    product = Product.objects.filter(id=pk).first()
    if product:
        try:
            cart = Cart.objects.get(user=request.user, product=product)
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart(user=request.user, product=product)
            cart.save()
    return redirect('cart')


@login_required(login_url='signin')
def update_cart(request,pk):
    cart = Cart.objects.filter(id=pk, user=request.user).first()
    if cart and request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.quantity = quantity
        cart.save()
    return redirect('cart')


@login_required(login_url='signin')
def remove_from_cart(request, pk):
    cart = Cart.objects.filter(id=pk, user=request.user).first()
    if cart:
        cart.delete()
    return redirect('cart')


def logout(request):
	auth.logout(request)
	return redirect('index')


def UserDetails(request):
    user_detail = UserProfile.objects.all()
    categories = Category.objects.all()
    return render(request,'user_view.html',{'users':user_detail,'categories':categories})


def ad_userdelete(request,pk):
    edit= UserProfile.objects.get(id=pk)
    edit.delete()
    return redirect('UserDetails')

@login_required(login_url='signin')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)  # Remove the [:1] filter
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

            return redirect('product_detail', product_id=product_id)

    return render(request, 'product_detail.html', {'product': product, 'cart_quantity': total_quantity, 'reviews': reviews, 'average_rating': average_rating})