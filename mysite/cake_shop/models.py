from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=25)
    first_name = models.CharField(null=True, blank=True, max_length=25)
    last_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True)
    avatar = models.ImageField(upload_to='avatar/', null=True)
    email = models.EmailField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=25)
    city = models.CharField(null=True, blank=True, max_length=25)
    address = models.TextField(null=True, blank=True)
    data_join = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class Bakery(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    country = models.CharField(null=True, blank=True, max_length=50)
    city = models.CharField(null=True, blank=True, max_length=50)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='bakeries/', null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='categories/', null=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=25, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    has = models.BooleanField(default=True)
    kg = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', null=True)

class Order(models.Model):
    ROLE_CHOICES = (
    ('active', 'active'),
    ('completed', 'completed'),
    ('canceled', 'canceled'),
    )
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=25, default='active')
    quantity = models.PositiveIntegerField(default=1)
    date_order = models.DateField(auto_now_add=True)
    date_complete = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.item.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price