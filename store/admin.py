from django.contrib import admin
from .models import Order,Product,OrderItem,ShippingAddress,Customer
# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customer)