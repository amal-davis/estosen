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

    # Fetch all categories
    models_with_images = ModelProfile.objects.all()

    return render(request, 'index.html', {'cart_quantity': total_quantity, 'categories': categories, 'carts': carts,'products': products, 'models_with_images': models_with_images})


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


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    categories = Category.objects.all()
    available_sizes = product.sizes.all()  # Get the sizes associated with the product

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

    return render(request, 'product_detail.html', {'product': product, 'cart_quantity': total_quantity, 'reviews': reviews, 'average_rating': average_rating, 'categories': categories, 'available_sizes': available_sizes})




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
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    # wishlist = Wishlist.objects.filter(user=request.user).first()
    return render(request, 'all_products.html', {'products': products,'cart_quantity': total_quantity, 'categories': categories})


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

                model_profile = ModelProfile.objects.create(
                    user=user,
                    phone_number=phone_no,
                    age=age,
                    height=height,
                    gender=gender,
                    is_approved=False

                )
                model_profile.save()

                # Handle model image uploads
                for file in request.FILES.getlist('image'):
                    image = ModelImage(image=file)
                    image.save()
                    model_profile.images.add(image)

                print('Model Registration Succeed....')
        else:
            messages.info(request,'Password doesnt match!!!!!')
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
    context = {'model_data':model_data}
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