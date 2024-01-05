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
from django import template
from django.http import JsonResponse
import razorpay
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.base import ContentFile
from django.utils.datastructures import MultiValueDictKeyError
from django.template import Library
from django.db import transaction






from .models import *
import random
import string
# Create your views here.


def index(request):
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    products = Product.objects.all()[:3]

    for product in products:
        product.reviews = Review.objects.filter(product=product)
        product.average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.stars_representation = stars(product.average_rating)

    # Fetch all categories (adjust based on your actual model)
    model_data = AnotherDatabaseModel.objects.all()
    models_with_images = ModelProfile.objects.all()
    swiper_contents = SwiperContent.objects.all()
    section1 = FashionSection.objects.first()
    section2 = FashionSection2.objects.first()
    fashion_contents = FashionContent.objects.all()
    
    blogs = Blog.objects.all()

    return render(request, 'index.html', {
        'cart_quantity': total_quantity,
        'categories': categories,
        'carts': carts,
        'products': products,
        'models_with_images': models_with_images,
        'model_data': model_data,
        'blogs': blogs,
        'swiper_contents': swiper_contents,
        'section1': section1, 
        'section2': section2,
        'fashion_contents':fashion_contents,
    })


def another_database_model_details(request, model_id):
    another_model = get_object_or_404(AnotherDatabaseModel, id=model_id)
    
    # Fetch associated ModelProfile data
    model_profile_data = another_model.model_profile
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)

    context = {
        'another_model': another_model,
        'model_profile_data': model_profile_data,
        'cart_quantity': total_quantity, 
        'categories': categories, 
        'carts': carts
    }

    return render(request, 'model_details_view.html', context)


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


registers = Library()
@registers.filter(name='star')
def star(value):
    full_stars = int(value)
    half_star = int((value - full_stars) * 2)
    empty_stars = 5 - full_stars - half_star
    return {'full_stars': range(full_stars), 'half_star': half_star, 'empty_stars': range(empty_stars)}



def categories(request, category_name):
    categories = Category.objects.all()
    reversed_orders = reversed(list(categories))
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    reversed_order = reversed(list(products))

    for product in products:
        product.reviews = Review.objects.filter(product=product)
        product.average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.stars_representation = stars(product.average_rating)

    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    context = {'category_name': category_name, 'cart_quantity': total_quantity, 'products': reversed_order, 'categories': reversed_orders}
    return render(request, 'category_page.html', context)


def productpage(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        select = request.POST['select']
        quantity = request.POST['quantity']
        has_sizes = request.POST.get('has_sizes')

        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 0

        category = Category.objects.get(id=select)

        # Create the product without saving it yet
        product = Product(name=name, category=category, description=description, price=price, quantity=quantity)
        
        # Save the product to get an ID
        product.save()

        # Handle sizes
        if has_sizes:
            sizes_input = request.POST.get('sizes', '')
            sizes_list = [size.strip() for size in sizes_input.split(',')]
            
            for size in sizes_list:
                product_size, created = ProductSize.objects.get_or_create(size=size)
                product.sizes.add(product_size)

        # Save the product again to update many-to-many relationships
        product.save()

        # Handle multiple file uploads
        for file in request.FILES.getlist('file'):
            image = Image_section(image=file)
            image.save()
            product.images.add(image)

        # Set status based on quantity
        if product.quantity == 0:
            product.status = 'Out of stock'
        elif product.quantity < 5:
            product.status = 'Limited stock'
        else:
            product.status = 'In stock'

        product.save()

        return redirect('productpage')

    categories = Category.objects.all()
    product_detail = Product.objects.all()
    reversed_orders = reversed(list(product_detail))
    return render(request, 'ad_product.html', {'categories': categories, 'product': reversed_orders})

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
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This Email already exists!')
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
                login(request, user)
                return redirect('admin_page')
            else:
                model_profile = ModelProfile.objects.filter(user=user).first()

                if model_profile:
                    if model_profile.is_approved:
                        # Model is approved, redirect to the model dashboard or any other page
                        login(request, user)
                        return redirect('model_dashboard')
                    else:
                        # Model is not approved, show a message
                        messages.warning(request, 'Your model profile is not yet approved. Please wait for admin approval.')
                        return redirect('login_page')
                else:
                    # Regular user, redirect to the index page
                    login(request, user)
                    return redirect('index')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login_page')

    return redirect('login_page')





@login_required(login_url='signin')
def cart(request):
    carts = Cart.objects.filter(user=request.user)
    categories = Category.objects.all()
    total_price = 0
    total_quantity = carts.aggregate(Sum('quantity'))['quantity__sum'] or 0
    grand_total = sum(cart.product.price * cart.quantity for cart in carts)
    subtotal = 0  # Initialize subtotal here

    for cart in carts:
        cart.subtotal = cart.product.price * cart.quantity
        total_price += cart.subtotal
        subtotal += cart.subtotal

    return render(request, 'cart.html', {'carts': carts, 'subtotal': subtotal, 'total_price': total_price, 'grand_total': grand_total, 'categories': categories, 'cart_quantity': total_quantity})

    

def get_first_available_size(product):
    if product.sizes.exists():
        return product.sizes.first()
    return None

@login_required(login_url='signin')
def add_to_cart(request, pk):
    product = Product.objects.filter(id=pk).first()

    if product:
        size = get_first_available_size(product)

        try:
            cart = Cart.objects.get(user=request.user, product=product, size=size)
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart(user=request.user, product=product, size=size)
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


register = Library()

@register.filter(name='stars')
def stars(value):
    full_stars = int(value)
    half_star = int((value - full_stars) * 2)
    empty_stars = 5 - full_stars - half_star
    return {'full_stars': range(full_stars), 'half_star': half_star, 'empty_stars': range(empty_stars)}



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    categories = Category.objects.all()
    available_sizes = product.sizes.all()  # Get the sizes associated with the product

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    stars_representation = stars(average_rating)

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

    return render(request, 'product_detail.html', {'product': product, 'cart_quantity': total_quantity, 'reviews': reviews, 'average_rating': average_rating, 'stars_representation': stars_representation, 'categories': categories, 'available_sizes': available_sizes})




def review_details(request):
    user_detail = UserProfile.objects.all()
    categories = Category.objects.all()
    review = Review.objects.all()
    return render(request,'admin_review.html',{'users':user_detail,'categories':categories,'review':review})


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    
    return redirect('review_details')


def allproducts(request):
    products = Product.objects.all()
    reversed_order = reversed(list(products))

    for product in products:
        product.reviews = Review.objects.filter(product=product)
        product.average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.stars_representation = stars(product.average_rating)

    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)

    return render(request, 'all_products.html', {'products': reversed_order, 'cart_quantity': total_quantity, 'categories': categories})


@login_required(login_url='signin')
def add_to_cart_details(request, pk):
    product = get_object_or_404(Product, id=pk)
    user = request.user
    cart_item = Cart.objects.filter(user=user, product=product).first()

    if request.method == 'POST':
        selected_size_id = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))
        
        # Assuming you have a ProductSize model for sizes
        selected_size = ProductSize.objects.get(id=selected_size_id) if selected_size_id else None

        if cart_item:
            cart_item.quantity += quantity
            cart_item.update_quantity_and_total()
        else:
            Cart.objects.create(user=user, product=product, quantity=quantity, size=selected_size)

        return redirect('cart')  # Replace 'your_app:view_cart' with the actual URL name for your cart page
    

def checkout_page(request):
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    return render(request,'checkout.html',{'categories':categories,'cart_quantity': total_quantity})


def checkout_view(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('adress')
        pincode = request.POST.get('pincode')
        state = request.POST.get('statae')
        email = request.POST.get('email')
        phone = request.POST.get('phone_no')

        # Check if the 'address' field is not empty
        if address:
            # Create a list to store order instances
            orders = []

            # Create an order for each item in the cart
            for cart_item in cart_items:
                order = Order.objects.create(
                    user=user,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_price=cart_item.product.price * cart_item.quantity,
                    size=cart_item.size,
                    name=name,
                    address=address,
                    pincode=pincode,
                    state=state,
                    email=email,
                    phone=phone,
                )
                orders.append(order)

            # Clear the user's cart after creating orders
            cart_items.delete()

            # Print debug statement
            print("Order created successfully")

            # Redirect to the confirmation page with the list of orders
            return render(request, 'confirmation.html', {'orders': orders, 'categories': categories})

        else:
            # Print debug statement
            print("Address is empty")

            # Handle the case where 'address' is empty
            return render(request, 'checkout.html', {'cart_items': cart_items, 'categories': categories, 'error_message': 'Address cannot be empty'})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'categories': categories})


def confirmation_page(request):
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)

    # Retrieve the latest order for the current user based on the creation timestamp
    latest_order = Order.objects.filter(user=user).latest('id')

    # Retrieve messages
    order_messages = messages.get_messages(request)

    total_sum = sum(order.total_price for order in Order.objects.filter(user=user))
    print("Total Sum:", total_sum) 
    print("Total Price of Latest Order:", latest_order.total_price)

    context = {
        'order': latest_order,
        'categories': categories,
        'cart_quantity': total_quantity,
        'order_messages': order_messages,
        'total_sum': total_sum
    }

    return render(request, 'confirmation.html', context)


def confirm_product(request):
    if request.method == 'POST':
        try:
            # Extract user information
            user_info = {
                'name': request.POST.get('name'),
                'address': request.POST.get('address'),
                'pincode': request.POST.get('pincode'),
                'state': request.POST.get('state'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
            }

            # Loop through each product in the order
            for i in range(int(request.POST.get('product_count', 0))):
                product_info = {
                    'product_name': request.POST.get(f'product_name_{i}'),
                    'quantity': int(request.POST.get(f'quantity_{i}', 0)),
                    'size': request.POST.get(f'size_{i}'),
                    'total_price': request.POST.get(f'total_price_{i}'),
                    'product_image': request.POST.get(f'product_image_{i}'),
                }

                # Create Order_section instance for each product
                order_instance = Order_sections.objects.create(
                    user=request.user,
                    name=user_info['name'],
                    address=user_info['address'],
                    pincode=user_info['pincode'],
                    state=user_info['state'],
                    email=user_info['email'],
                    phone=user_info['phone'],
                    product_name=product_info['product_name'],
                    quantity=product_info['quantity'],
                    size=product_info['size'],
                    total_price=product_info['total_price'],
                    product_image=product_info['product_image'],
                )

                # Fetch the corresponding product
                product = Product.objects.get(name=product_info['product_name'])

                # Update the product quantity
                if product.quantity is not None:
                    new_quantity = int(product.quantity) - product_info['quantity']
                    if new_quantity >= 0:
                        product.quantity = new_quantity
                        product.update_status()
                        product.save()
                    else:
                        order_instance.delete()
                        return HttpResponse("Insufficient quantity")

            return redirect('payment_confirmation_page')

        except Exception as e:
            # Handle exceptions and display an error message if necessary
            print(e)
            return HttpResponse("An error occurred while processing the order")

    return HttpResponse("Invalid request method")



def payment_confirmation_page(request):
    return render(request , 'payment_confirmation_page.html')



def order_admin(request):
    # Retrieve orders from your model (Order_sections)
    orders = Order_sections.objects.all()

    # Reverse the order of the list
    reversed_orders = reversed(list(orders))

    return render(request, 'order_admin.html', {'orders': reversed_orders})

def order_page(request):
    user_orders = Order_sections.objects.filter(user=request.user)
    reversed_orders = reversed(list(user_orders))
    return render(request, 'user_order.html',{'user_orders':reversed_orders})

def update_order_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order_sections.objects.get(id=order_id)
        order.status = status
        order.save()
    return redirect('order_admin')



def model_registration(request):
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    return render(request,'model_registration.html',{'categories':categories,'cart_quantity': total_quantity})


def model_dashboard(request):
    # Check if the user is authenticated
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    if request.user.is_authenticated:
        try:
            # Retrieve the model profile associated with the user
            model_profile = ModelProfile.objects.get(user=request.user)

            # Retrieve only images associated with the current model profile
            model_images = model_profile.images.all()

            return render(request, 'model_dashboard.html', {'model_profile': model_profile, 'model_images': model_images,'categories':categories,'cart_quantity': total_quantity})
        except ModelProfile.DoesNotExist:
            # If the user doesn't have a model profile, handle accordingly
            return render(request, 'model_dashboard.html', {'error_message': 'Model profile not found.'})
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('login_page')


def modelcreate(request):
    if request.method == 'POST':
        # Extract model registration data from the form
        first_name = request.POST['fname']
        last_name = request.POST['sname']
        username = request.POST['uname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']

        # Additional model-specific fields
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        Chest_round = request.POST['Chest_round']
        Shoulder_to_shoulder = request.POST['Shoulder_to_shoulder']
        Hip_round = request.POST['Hip_round']
        Arm_hole = request.POST['Arm_hole']
        Waist_round = request.POST['Waist_round']
        
        # Initialize dictionary to store gender-specific measurements
        measurements = {}

        if gender == 'Men':
            # Men's measurements
            
# Men's measurements
         measurements['neck'] = request.POST['neck']
         measurements['Full_sleeves_length'] = request.POST['Full_sleeves_length']
         measurements['Half_sleeves_length'] = request.POST['Half_sleeves_length']
         measurements['Biceps'] = request.POST.getlist('Biceps')[0].strip() if request.POST.getlist('Biceps') else None


         measurements['Lower_waist'] = request.POST['Lower_waist']
         measurements['Trouser_length'] = request.POST['Trouser_length']
         measurements['Trouser_Bottom'] = request.POST['Trouser_Bottom']
         measurements['Denim_length'] = request.POST['Denim_length']
         measurements['Thigh'] = request.POST['Thigh']
         measurements['Shirt_size'] = request.POST['Shirt_size']
         measurements['T_Shirt'] = request.POST['T_Shirt']
         measurements['Shoe_size'] = request.POST.getlist('Shoe_size')[0].strip() if request.POST.getlist('Shoe_size') else None

         measurements['Crotch_Length'] = request.POST['Crotch_Length']

         print(request.POST)
         



        elif gender == 'Female'or gender == 'Trans':
    # Female or Trans measurements
           measurements['Shoulder_to_waistline'] = request.POST['Shoulder_waistline']
           measurements['Shoulder_to_floor'] = request.POST['Shoulder_floor']
           measurements['Neck_round'] = request.POST['Neck_rounds']
           measurements['Upper_Bust'] = request.POST['Upper_Busts']
           measurements['Full_Bust'] = request.POST['Full_Busts']
           measurements['Below_Bust'] = request.POST['Below_Buste']
           measurements['Lower_waist_round'] = request.POST['Lower_round']
           measurements['Full_length_sleeves'] = request.POST['Full_sleeves']
           measurements['Half_sleeve'] = request.POST['Half_sleeves']
           measurements['3_4_sleeve'] = request.POST['3/4_sleeves']
           measurements['Sleeves_round'] = request.POST['Sleeves_rounds']
           measurements['Biceps'] = request.POST.getlist('Bicep')[0].strip() if request.POST.getlist('Biceps') else None
           measurements['Shoulder_to_knee'] = request.POST['Shoulder_knee']
           measurements['Knee_round'] = request.POST['Knee_rounds']
           measurements['Thigh_round'] = request.POST['Thigh_rounds']
           measurements['Ankle_round'] = request.POST['Ankle_rounds']
           measurements['crotch_point'] = request.POST['crotch_points']
           measurements['Shoe_size'] = request.POST.getlist('Shoe_sizes')[0].strip() if request.POST.getlist('Shoe_size') else None
           
           



        elif gender == 'Kid Boy':
            # Kid Boy measurements
            measurements['Shoulder_to_waistline'] = request.POST['Shoulder_to_waistlines']
            measurements['Shoulder_to_floor'] = request.POST['Shoulder_to_floors']
            measurements['Shoulder_to_hip'] = request.POST['Shoulder_to_hip']
            measurements['Neck_round'] = request.POST['Necks']
            measurements['Upper_Bust'] = request.POST['Upper_Buste']
            measurements['shorts'] = request.POST['short']
            measurements['Lower_waist_round'] = request.POST['Lower_waist']
            measurements['Full_length_sleeves'] = request.POST['Full_length']
            measurements['Half_sleeve'] = request.POST['Half_sleev']
            measurements['3_4_sleeve'] = request.POST['3/4_sleevese']
            measurements['Elbow_round'] = request.POST['Elbow_round']
            measurements['Elbow_length'] = request.POST['Elbow_length']
            measurements['Biceps'] = request.POST['Bicepse']
            measurements['Shoulder_to_knee'] = request.POST['Shoulder_to']
            measurements['Knee_round'] = request.POST['Knee_roundse']
            measurements['Thigh_round'] = request.POST['Thigh_roundse']
            measurements['Ankle_round'] = request.POST['Ankle_roundse']
            measurements['crotch_point'] = request.POST['crotch_pointse']
            measurements['Shoe_size'] = request.POST['Shoe']
            measurements['Lower_waist_to'] = request.POST['Lower_waist_to']
            measurements['trouser_length'] = request.POST['trouser_length']
            print("Measurements:", measurements)

        elif gender == 'Kid Girl':
            # Kid Girl measurements
            measurements['Shoulder_to_waistline'] = request.POST['Shoulder_to_waistline']
            measurements['Shoulder_to_floor'] = request.POST['Shoulder_to_floor']
            measurements['Neck_round'] = request.POST['Neck_round']
            measurements['Upper_Bust'] = request.POST['Upper_Bust']
            measurements['Full_Bust'] = request.POST['Full_Bust']
            measurements['Below_Bust'] = request.POST['Below_Bust']
            measurements['Lower_waist_round'] = request.POST['Lower_waist_round']
            measurements['Full_length_sleeves'] = request.POST['Full_length_sleeves']
            measurements['Half_sleeve'] = request.POST['Half_sleeve']
            measurements['3_4_sleeve'] = request.POST['3/4_sleeve']
            measurements['Sleeves_round'] = request.POST['Sleeves_round']
            measurements['Biceps'] = request.POST['Biceps']
            measurements['Shoulder_to_knee'] = request.POST['Shoulder_to_knee']
            measurements['Knee_round'] = request.POST['Knee_round']
            measurements['Thigh_round'] = request.POST['Thigh_round']
            measurements['Ankle_round'] = request.POST['Ankle_round']
            measurements['crotch_point'] = request.POST['crotch_point']
            measurements['Shoe_size'] = request.POST['Shoe_size']
            measurements['Waist_to_Knee'] = request.POST['Waist_to_Knee']

        else:
            messages.info(request, 'Invalid gender selection!')
            return redirect('model_registration')

        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This Email already exists!')
                return redirect('signup_page')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email
                )
                user.save()

                # Create User and ModelProfile instances
                model_profile = ModelProfile.objects.create(
                    user=user,
                    phone_number=phone_no,
                    age=age,
                    height=height,
                    gender=gender,
                    weight=weight,
                    Chestround=Chest_round,
                    Shouldertoshoulder=Shoulder_to_shoulder,
                    Hipround=Hip_round,
                    Armhole=Arm_hole,
                    Waistround=Waist_round,
                    is_approved=False
                )

                # Populate additional gender-specific measurements
                if gender == 'Men':
                    model_profile.men_measurements = measurements
                elif gender == 'Female' or gender == 'Trans':
                    model_profile.female_measurements = measurements
                elif gender == 'Kid Boy':
                    model_profile.kid_boy_measurements = measurements
                elif gender == 'Kid Girl':
                    model_profile.kid_girl_measurements = measurements

                # Save the model_profile instance
                model_profile.save()

                # Handle model image uploads
                for file in request.FILES.getlist('image'):
                    image = ModelImage(image=file)
                    image.save()
                    model_profile.images.add(image)

                print('Model Registration Succeed....')
        else:
            messages.info(request, 'Password doesn\'t match!!!!!')
            print('Password is not matching')
            return redirect('model_registration')

        return redirect('login_page')
    else:
        return render(request, 'model_registration.html')


def model_edit(request,pk):
    if request.method == 'POST':
        model = ModelProfile.objects.get(id=pk)
        user = model.user
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('sname')
        user.email = request.POST.get('email')
        user.username = request.POST.get('uname')
        model.phone_number = request.POST.get('phone_no')
        model.age = request.POST.get('age')
        model.height = request.POST.get('height')
        model.weight = request.POST.get('weight')
        model.Chestround = request.POST.get('Chest_round')
        model.Shouldertoshoulder = request.POST.get('Shoulder_to_shoulder')
        model.Hipround = request.POST.get('Hip_round')
        model.Armhole = request.POST.get('Armhole')
        model.Waistround = request.POST.get('Waist_round')
        model.gender = request.POST.get('gender')
        measurements = {}
        if model.gender == 'Men':
            measurements['neck'] = request.POST['neck']
            measurements['Full_sleeves_length'] = request.POST.get('Full_sleeves_length')
            measurements['Half_sleeves_length'] = request.POST.get('Half_sleeves_length')
            measurements['Biceps'] = request.POST.get('Biceps')


            measurements['Lower_waist'] = request.POST.get('Lower_waist')
            measurements['Trouser_length'] = request.POST.get('Trouser_length')
            measurements['Trouser_Bottom'] = request.POST.get('Trouser_Bottom')
            measurements['Denim_length'] = request.POST.get('Denim_length')
            measurements['Thigh'] = request.POST.get('Thigh')
            measurements['Shirt_size'] = request.POST.get('Shirt_size')
            measurements['T_Shirt'] = request.POST.get('T_Shirt')
            measurements['Shoe_size'] = request.POST.get('Shoe_size')
            measurements['Crotch_Length'] = request.POST.get('Crotch_Length')

        elif model.gender == 'Female' or model.gender == 'Trans':
             measurements['Shoulder_to_waistline'] = request.POST.get('Shoulder_waistline')
             measurements['Shoulder_to_floor'] = request.POST.get('Shoulder_floor')
             measurements['Neck_round'] = request.POST.get('Neck_rounds')
             measurements['Upper_Bust'] = request.POST.get('Upper_Busts')
             measurements['Full_Bust'] = request.POST.get('Full_Busts')
             measurements['Below_Bust'] = request.POST.get('Below_Buste')
             measurements['Lower_waist_round'] = request.POST.get('Lower_round')
             measurements['Full_length_sleeves'] = request.POST.get('Full_sleeves')
             measurements['Half_sleeve'] = request.POST.get('Half_sleeves')
             measurements['3_4_sleeve'] = request.POST.get('3/4_sleeves')
             measurements['Sleeves_round'] = request.POST.get('Sleeves_rounds')
             measurements['Biceps'] = request.POST.get('Bicep')
             measurements['Shoulder_to_knee'] = request.POST.get('Shoulder_knee')
             measurements['Knee_round'] = request.POST.get('Knee_rounds')
             measurements['Thigh_round'] = request.POST.get('Thigh_rounds')
             measurements['Ankle_round'] = request.POST.get('Ankle_rounds')
             measurements['crotch_point'] = request.POST.get('crotch_points')
             measurements['Shoe_size'] = request.POST.get('Shoe_sizes')
        elif model.gender == 'Kid Boy':
             measurements['Shoulder_to_waistline'] = request.POST.get('Shoulder_to_waistlines')
             measurements['Shoulder_to_floor'] = request.POST.get('Shoulder_to_floors')
             measurements['Shoulder_to_hip'] = request.POST.get('Shoulder_to_hip')
             measurements['Neck_round'] = request.POST.get('Necks')
             measurements['Upper_Bust'] = request.POST.get('Upper_Buste')
             measurements['shorts'] = request.POST.get('short')
             measurements['Lower_waist_round'] = request.POST.get('Lower_waist')
             measurements['Full_length_sleeves'] = request.POST.get('Full_length')
             measurements['Half_sleeve'] = request.POST.get('Half_sleev')
             measurements['3_4_sleeve'] = request.POST.get('3/4_sleevese')
             measurements['Elbow_round'] = request.POST.get('Elbow_round')
             measurements['Elbow_length'] = request.POST.get('Elbow_length')
             measurements['Biceps'] = request.POST.get('Bicepse')
             measurements['Shoulder_to_knee'] = request.POST.get('Shoulder_to')
             measurements['Knee_round'] = request.POST.get('Knee_roundse')
             measurements['Thigh_round'] = request.POST.get('Thigh_roundse')
             measurements['Ankle_round'] = request.POST.get('Ankle_roundse')
             measurements['crotch_point'] = request.POST.get('crotch_pointse')
             measurements['Shoe_size'] = request.POST.get('Shoe')
             measurements['Lower_waist_to'] = request.POST.get('Lower_waist_to')
             measurements['trouser_length'] = request.POST.get('trouser_length')
        elif model.gender == 'Kid Girl':
            measurements['Shoulder_to_waistline'] = request.POST.get('Shoulder_to_waistline')
            measurements['Shoulder_to_floor'] = request.POST.get('Shoulder_to_floor')
            measurements['Neck_round'] = request.POST.get('Neck_round')
            measurements['Upper_Bust'] = request.POST.get('Upper_Bust')
            measurements['Full_Bust'] = request.POST.get('Full_Bust')
            measurements['Below_Bust'] = request.POST.get('Below_Bust')
            measurements['Lower_waist_round'] = request.POST.get('Lower_waist_round')
            measurements['Full_length_sleeves'] = request.POST.get('Full_length_sleeves')
            measurements['Half_sleeve'] = request.POST.get('Half_sleeve')
            measurements['3_4_sleeve'] = request.POST.get('3/4_sleeve')
            measurements['Sleeves_round'] = request.POST.get('Sleeves_round')
            measurements['Biceps'] = request.POST.get('Biceps')
            measurements['Shoulder_to_knee'] = request.POST.get('Shoulder_to_knee')
            measurements['Knee_round'] = request.POST.get('Knee_round')
            measurements['Thigh_round'] = request.POST.get('Thigh_round')
            measurements['Ankle_round'] = request.POST.get('Ankle_round')
            measurements['crotch_point'] = request.POST.get('crotch_point')
            measurements['Shoe_size'] = request.POST.get('Shoe_size')
            measurements['Waist_to_Knee'] = request.POST.get('Waist_to_Knee')
        
        model.men_measurements = measurements if model.gender == 'Men' else None
        model.female_measurements = measurements if model.gender == 'Female' or model.gender == 'Trans' else None
        model.kid_boy_measurements = measurements if model.gender == 'Kid Boy' else None
        model.kid_girl_measurements = measurements if model.gender == 'Kid Girl' else None
             
             
        
        old_images = list(model.images.all())
        new_images = request.FILES.getlist('image')
        if old_images and not new_images:
            # Keep the existing images
            model.images.set(old_images)
        elif new_images:
            # Update the images
            new_image_objects = [ModelImage.objects.create(image=image) for image in new_images]
            model.images.set(new_image_objects)
        model.save()
        user.save()
        return redirect('model_dashboard')
    model = ModelProfile.objects.get(id=pk)
    return render(request,'model_edit.html',{'user':model})




def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('cpassword')
        new_password = request.POST.get('password')
        confirm_new_password = request.POST.get('password_confirm')

        if request.user.check_password(current_password):
            if new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()

                update_session_auth_hash(request, request.user)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('index')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')
    return render(request, 'update_password.html')



def model_details(request):
    model_data = ModelProfile.objects.all()
    reversed_orders = reversed(list(model_data))
    context = {'model_data':reversed_orders}
    return render(request, 'model_details.html',context)


def approve_model(request, model_id):
    model_profile = get_object_or_404(ModelProfile, id=model_id)
    model_profile.is_approved = True
    model_profile.save()
    return redirect('model_details')  # Update with the correct URL name

def disapprove_model(request, model_id):
    model_profile = get_object_or_404(ModelProfile, id=model_id)
    model_profile.is_approved = False
    model_profile.save()
    return redirect('model_details')



def save_image_to_another_database(request):
    if request.method == 'POST':
        try:
            # Extract values from the form
            username = request.POST.get('username')
            image_id = request.POST.get('image_id')
            email = request.POST.get('email')
            phoneno = request.POST.get('phone_no')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            chestround = request.POST.get('chestround')
            shouldertoshoulder = request.POST.get('shouldertoshoulder')
            hipround = request.POST.get('hipround')
            armhole = request.POST.get('armhole')
            waistround = request.POST.get('waistround')

            # Validate numeric fields
            if not chestround:
                print("Chestround value is empty.")
                return HttpResponse('Chestround value is empty.')

            try:
                chestround = float(chestround)
            except ValueError:
                print("Invalid Chestround value:", chestround)
                return HttpResponse('Invalid Chestround value.')

            # Repeat similar validation for other numeric fields...

            # Retrieve the image from the ModelImage model
            try:
                image = ModelImage.objects.get(id=image_id)
            except ModelImage.DoesNotExist:
                print("Image not found with ID:", image_id)
                return HttpResponse('Image not found with the given ID.')

            # Save to another database
            another_db_instance = AnotherDatabaseModel(
                username=username,
                image=image,
                email=email,
                phone_no=phoneno,
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                Chestround=chestround,
                Shouldertoshoulder=shouldertoshoulder,
                Hipround=hipround,
                Armhole=armhole,
                Waistround=waistround
            )
            another_db_instance.save()

            # You can also redirect the user to another page after successful submission
            return redirect('model_details')

        except Exception as e:
            print("Error:", e)
            return HttpResponse('Error occurred during form submission.')

    # Handle GET requests if needed
    return HttpResponse('Invalid request method.')


def delete_model_view(request, model_id):
    model_instance = get_object_or_404(ModelProfile, id=model_id)

    # Delete related user data
    user_instance = model_instance.user
    user_instance.delete()

    # Delete the model instance
    model_instance.delete()

    return redirect('model_details')


def model_image_control(request):
    model_control = AnotherDatabaseModel.objects.all()
    context = {'model_control':model_control}
    return render(request, 'model_image_control.html',context)


def delete_model_profile(request, pk):
    profile_to_delete = get_object_or_404(AnotherDatabaseModel, pk=pk)

    # Delete associated images if needed
    if profile_to_delete.image:
        profile_to_delete.image.delete()

    # Delete the profile
    profile_to_delete.delete()

    return redirect('model_image_control')


def add_blog(request):
    blogs = Blog.objects.all()
    return render(request,'add_blog.html',{'blogs': blogs})


def save_blog_section(request):
    if request.method == 'POST':
        try:
            # Extract values from the form
            title = request.POST.get('title')
            author = request.POST.get('author')
            content = request.POST.get('content')
            image = request.FILES.get('image')  # Assuming the image is a file field

            # Validate required fields
            if not title or not author or not content:
                print("Title, author, or content is empty.")
                return HttpResponse('Title, author, or content is empty.')

            # Create a new blog instance
            new_blog = Blog(
                title=title,
                author=author,
                content=content,
                image=image
            )

            # Save the blog to the database
            new_blog.save()

            # Redirect the user to another page after successful submission
            return redirect('add_blog')  # Change 'blog_list' to the URL name of your blog listing view

        except Exception as e:
            print("Error:", e)
            return HttpResponse('Error occurred during form submission.')

    # Handle GET requests if needed
    return HttpResponse('Invalid request method.')


def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    
    if blog.image:
       blog.image.delete()
    blog.delete()
    return redirect('add_blog')
 

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        # Extract values from the form
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Validate required fields
        if not title or not author or not content:
            return HttpResponse('Title, author, or content is empty.')

        # Update the blog instance
        blog.title = title
        blog.author = author
        blog.content = content
        if image:
            blog.image = image

        # Save the changes
        blog.save()

        return redirect('add_blog')  # Redirect to the blog list view
    else:
        # Render the edit form with existing data
        return render(request, 'edit_blog.html', {'blog': blog})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog_details.html', {'blog': blog})


def web_image_section(request):
    return render(request,'web_image_section.html')


def slider_content_add(request):
    swiper_contents = SwiperContent.objects.all()
    return render(request,'slider_content_add.html',{'swiper_contents': swiper_contents})


def save_slider_content(request):
    if request.method == 'POST':
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        button_text = request.POST.get('button_text')
        button_link = request.POST.get('button_link')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        SwiperContent.objects.create(
            heading=heading,
            description=description,
            button_text=button_text,
            button_link=button_link,
            image=image,
            video=video
        )
        
        return redirect('slider_content_add')  # Redirect to the same page after successful submission

    return render(request, 'slider_content_add.html')


def delete_slider_content(request, content_id):
    content = get_object_or_404(SwiperContent, pk=content_id)
    content.delete()

    return redirect('slider_content_add')


def edit_slider_content(request, content_id):
    content = get_object_or_404(SwiperContent, pk=content_id)

    if request.method == 'POST':
        # Update the existing content
        content.heading = request.POST.get('heading', '')
        content.description = request.POST.get('description', '')
        content.button_text = request.POST.get('button_text', '')
        content.button_link = request.POST.get('button_link', '')

        # Handle image and video fields separately, as they might not be present in every request
        image = request.FILES.get('image')
        if image:
            content.image = image

        video = request.FILES.get('video')
        if video:
            content.video = video

        content.save()

        return redirect('slider_content_add')  # Redirect to the same page after successful submission

    return render(request, 'edit_slider_content.html', {'content': content})


def fashion_section(request):
    section_id = 1 
    sections_id = 2 
    section1_data = FashionSection.objects.all()
    section2_data = FashionSection2.objects.all()
    return render(request,'add_fashion_section.html', {'section_id': section_id,'sections_id': sections_id,'section1_data': section1_data, 'section2_data': section2_data})




def add_fashion_section(request, section_id):
    if request.method == 'POST':
        heading = request.POST.get('heading', '')
        paragraph = request.POST.get('paragraph', '')
        button_text = request.POST.get('button_text', '')
        button_link = request.POST.get('button_link', '')
        image = request.FILES.get('image')

        if section_id == 1:
            FashionSection.objects.create(
                heading=heading,
                paragraph=paragraph,
                button_text=button_text,
                button_link=button_link,
                image=image
            )
        elif section_id == 2:
            FashionSection2.objects.create(
                heading=heading,
                paragraph=paragraph,
                button_text=button_text,
                button_link=button_link,
                image=image
            )

        return redirect('fashion_section')

    return render(request, 'add_fashion_section.html', {'section_id': section_id})





def delete_fashion_entry(request, section_id, entry_id):
    if section_id == 1:
        entry = get_object_or_404(FashionSection, pk=entry_id)
        entry.delete()
    elif section_id == 2:
        entry = get_object_or_404(FashionSection2, pk=entry_id)
        entry.delete()

    return redirect('fashion_section')



def edit_fashion_entry(request, section_id, entry_id):
    # Retrieve the entry based on the section_id
    entry = FashionSection.objects.get(pk=entry_id) if section_id == 1 else FashionSection2.objects.get(pk=entry_id)

    if request.method == 'POST':
        # Update the entry based on the submitted data
        entry.heading = request.POST.get('heading', '')
        entry.paragraph = request.POST.get('paragraph', '')
        entry.button_text = request.POST.get('button_text', '')
        entry.button_link = request.POST.get('button_link', '')
        entry.image = request.FILES.get('image')
        entry.save()

        # Redirect to the fashion_section view after successful update
        return redirect('fashion_section')

    return render(request, 'edit_fashion_entry.html', {'entry': entry, 'section_id': section_id})



def fashion_check_section(request):
    if request.method == 'POST':
        # Process form submission
        image = request.FILES.get('image')
        heading = request.POST.get('heading', '')
        title = request.POST.get('title', '')
        button_text = request.POST.get('button_text', '')
        button_link = request.POST.get('button_link', '')
        background_color = request.POST.get('background_color', '')

        # Save to the database
        FashionContent.objects.create(
            image=image,
            heading=heading,
            title=title,
            button_text=button_text,
            button_link=button_link,
            background_color=background_color
        )

        return redirect('fashion_check_section')  # Redirect to the same page or another page after submission

    # Fetch existing data
    fashion_contents = FashionContent.objects.all()

    return render(request, 'check_section.html', {'fashion_contents': fashion_contents})



def edit_fashion_content(request, content_id):
    item = get_object_or_404(FashionContent, pk=content_id)

    if request.method == 'POST':
        # Process the form submission for editing


        # Update the existing item in the database
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.heading = request.POST.get('heading', '')
        item.title = request.POST.get('title', '')
        item.button_text = request.POST.get('button_text', '')
        item.button_link =  request.POST.get('button_link', '')
        item.background_color = request.POST.get('background_color', '')
        item.save()

        return redirect('fashion_check_section')  # Redirect to the same page or another page after editing

    return render(request, 'edit_fashion_content.html', {'item': item})


def delete_fashion_content(request, content_id):
    item = get_object_or_404(FashionContent, pk=content_id)
    item.delete()
    return redirect('fashion_check_section')
