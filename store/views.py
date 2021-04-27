from django.shortcuts import render
from .models import Order,Product,OrderItem,ShippingAddress,Customer
from django.http import JsonResponse
import json
import datetime
from .utils import *
#from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def store(request):
     data=cartData(request)

     cartItems=data['cartItems']
     order=data['order']
     items=data["items"] 

     products=Product.objects.all()
     context={"products":products,'cartItems':cartItems}
     return render(request,"store/store.html",context)

def cart(request):
     data=cartData(request)

     cartItems=data['cartItems']
     order=data['order']
     items=data["items"] 
     context={"items":items,"order":order,'cartItems':cartItems,'shipping':False }
     return render(request,"store/cart.html",context)

def checkout(request):
     data=cartData(request)

     cartItems=data['cartItems']
     order=data['order']
     items=data["items"] 
 
     context={"items":items,"order":order,'cartItems':cartItems }
     return render(request,"store/checkout.html",context)
    
def updateItem(request):
    data=json.loads(request.body)
    productid=data['productid']
    action=data['action']
    customer=request.user.customer
    product=Product.objects.get(id=productid)
    order,created=Order.objects.get_or_create(customer=customer,complete=False) 
    orderitem ,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
         orderitem.quantity=(orderitem.quantity+1)
    elif action=="remove":
         orderitem.quantity=(orderitem.quantity-1)
    orderitem.save()

    if orderitem.quantity <= 0 :
       orderitem.delete()      
        
    return JsonResponse('item was added',safe=False)

#@csrf_exempt
def processOrder(request):
     transction_id=datetime.datetime.now().timestamp()
     data=json.loads(request.body)
     if request.user.is_authenticated:
          customer=request.user.customer
          order,created=Order.objects.get_or_create(customer=customer,complete=False) 
     else:
         customer,order=guestOrder(request ,data)
     total=float(data['form']['total'])
     order.transction_id=transction_id
     if total== order.get_cart_total:
          order.complete=True
     order.save()
     if order.shipping== True:
          ShippingAddress.objects.create(
               customer=customer,
               order=order,
               address=data['shipping']['address'],
               city=data['shipping']['city'],
               state=data['shipping']['state'],
               zipcode=data['shipping']['zipcode'],

          )
     return JsonResponse('payment complete',safe=False)