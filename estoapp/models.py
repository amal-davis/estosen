from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/', blank=True, null=True)




class Image_section(models.Model):
    image = models.ImageField(upload_to='product_images/')


class ProductSize(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size




class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField(Image_section, blank=True)
    status = models.CharField(max_length=20, default='In stock')  # Default status is 'In stock'
    quantity = models.CharField(max_length=255,null=True,blank=True)
    sizes = models.ManyToManyField(ProductSize, blank=True)
    
    def __str__(self):
        return self.name
    
    def update_status(self):
        if self.quantity == 0:
            self.status = 'Out of stock'
        elif self.quantity < 5:
            self.status = 'Limited stock'
        else:
            self.status = 'In stock'
        self.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True)


    def update_quantity_and_total(self):
        self.quantity += 1
        self.save()

        # Update grand total based on the updated quantity and product price
        self.product.refresh_from_db()  # Refresh the product instance to get the latest price
        self.save()
    
    


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)




class ModelImage(models.Model):
    image = models.ImageField(upload_to='model_images/')


class ModelProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    age = models.IntegerField()
    height = models.FloatField()
    images = models.ManyToManyField(ModelImage, blank=True)
    gender = models.CharField(max_length=150, blank=True)
    is_approved = models.BooleanField(default=False)  # New field
    weight = models.FloatField(default=0.0)
    Chestround = models.FloatField(default=0.0)
    Shouldertoshoulder = models.FloatField(default=0.0)
    Hipround =  models.FloatField(default=0.0)
    Armhole = models.FloatField(default=0.0)
    Waistround = models.FloatField(default=0.0)
    men_measurements = models.JSONField(blank=True, null=True)
    female_measurements = models.JSONField(blank=True, null=True)
    kid_boy_measurements = models.JSONField(blank=True, null=True)
    kid_girl_measurements = models.JSONField(blank=True, null=True)
    # Add other model-related fields

    def __str__(self):
        return self.user.username


class AnotherDatabaseModel(models.Model):
    model_profile = models.ForeignKey(ModelProfile, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(ModelImage, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, default='')
    phone_no = models.CharField(max_length=255, blank=True, default='')
    gender = models.CharField(max_length=255, blank=True, default='')
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    Chestround = models.FloatField(default=0.0)
    Shouldertoshoulder = models.FloatField(default=0.0)
    Hipround =  models.FloatField(default=0.0)
    Armhole = models.FloatField(default=0.0)
    Waistround = models.FloatField(default=0.0)




    def __str__(self):
        return self.username



class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Order_sections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=255,blank=True,)
    address = models.CharField(max_length=255,blank=True,)
    pincode = models.CharField(max_length=255,blank=True,)
    state = models.CharField(max_length=255,blank=True)
    email = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=255,blank=True)
    product_name = models.CharField(max_length=255,blank=True)
    quantity = models.CharField(max_length=255,blank=True)
    size = models.CharField(max_length=255,blank=True)
    total_price = models.CharField(max_length=255,blank=True)
    product_image = models.URLField()
    status = models.CharField(max_length=20, default='Pending') 



class SwiperContent(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.URLField()
    image = models.ImageField(upload_to='swiper_images/')
    video = models.FileField(upload_to='swiper_videos/', null=True, blank=True)


class FashionSection(models.Model):
    heading = models.CharField(max_length=255)
    paragraph = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.URLField()
    image = models.ImageField(upload_to='fashion_section/')

class FashionSection2(models.Model):
    heading = models.CharField(max_length=255)
    paragraph = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.URLField()
    image = models.ImageField(upload_to='fashion_section2/')

class FashionContent(models.Model):
    image = models.ImageField(upload_to='fashion_images/')
    heading = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    button_text = models.CharField(max_length=50)
    button_link = models.URLField()
    background_color = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.heading




    
    
    
    
