from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    shipping_email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address {str(self.id)}'

# Create a user profile by default when user sign up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
# Automate the profile creation
post_save.connect(create_profile, sender=User)


# Categories of Product
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# All of our products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    # Add Sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name

# Order model
class ShippingOrder(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank = True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'

# Auto add shipping date
@receiver(pre_save, sender=ShippingOrder)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now

# Create Order Items Model
class OrderItem(models.Model):
    # Foreign Keys
    order = models.ForeignKey(ShippingOrder, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'