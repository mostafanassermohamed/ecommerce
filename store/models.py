from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def image_upload(instance, filename):
    imagename , extension = filename.split('.')
    return "products/%s.%s"%(instance.id, extension)

class Customer(models.Model):
    user=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField( max_length=50,null=True)
    email=models.EmailField( max_length=254,null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(null=True, max_length=50)
    price=models.DecimalField(max_digits=7,decimal_places=2)
    digital=models.BooleanField(default=False,null=True, blank=False)
    image =models.ImageField(upload_to=image_upload,null=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            return self.image.url
        except :
            url=''
            return url
       

    
class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True, blank=False)
    transction_id=models.CharField(null=True, max_length=200)
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping= False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital== False:
               shipping=True
            
        return shipping 


    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    date_added=models.DateField( auto_now_add=True)
    quantity=models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total=self.quantity * self.product.price
        return total


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    address=models.CharField(null=False, max_length=200)
    city=models.CharField(null=False, max_length=200)
    state=models.CharField(null=False, max_length=200)
    zipcode=models.CharField(null=False, max_length=200)
    date_added=models.DateField( auto_now_add=True)
    def __str__(self):
        return self.address

    


    


   
