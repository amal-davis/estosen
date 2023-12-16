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


from .models import *
import random
import string
# Create your views here.


def index(request):
    categories = Category.objects.all()
    return render(request,'index.html',{'categories':categories})


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
    context = {'category_name': category_name, 'products': products,'categories':categories}
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


def product_list(request):
    # Get the sort option from the request
    sort_option = request.GET.get('sort', 'az')  # Default sort option is A to Z

    # Define the default ordering
    ordering = 'name'

    # Update ordering based on the sort option
    if sort_option == 'za':
        ordering = '-name'  # Z to A
    elif sort_option == 'low':
        ordering = 'price'  # Price Low to High
    elif sort_option == 'high':
        ordering = '-price'  # Price High to Low

    # Fetch the products from the database, sorted based on the selected option
    products = Product.objects.all().order_by(ordering)

    return render(request, 'product_list.html', {'products': products, 'sort_option': sort_option})
