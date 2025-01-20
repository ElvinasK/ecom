from django.contrib import admin
from .models import Category, Product, Profile, ShippingOrder, OrderItem
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(ShippingOrder)
admin.site.register(OrderItem)

# create an OrderItem InLine
class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = ShippingOrder
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address","amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInLine]

# Unregister ShippingOrder model
admin.site.unregister(ShippingOrder)

# Re-Register our Order and OrderAdmin
admin.site.register(ShippingOrder, OrderAdmin)


# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name' 'email']
    inlines = [ProfileInline]

# Unregister
admin.site.unregister(User)
# Re-Register
admin.site.register(User, UserAdmin)