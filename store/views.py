from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json,datetime
from .utils import *
# Create your views here.

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    cartitems = data['cartitems']
    context = {'products':products,'cartitems':cartitems}
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartitems = data['cartitems']
    context = {'items':items,'order':order,'cartitems':cartitems}
    return render(request,'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartitems = data['cartitems']
    context = {'items':items,'order':order,'cartitems':cartitems}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId," ",action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    
    if(action=='add'):
        orderItem.quantity+=1
    elif (action=='remove'):
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    return JsonResponse("Item was added!",safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
       
    else:
       customer , order = guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if (total==float(order.get_cart_total)):
        order.complete=True
    else:
        print("Form Total: ",total)
        print("Original Total: ",order.get_cart_total)
        print("Total is not equal")
    order.save()
    if(order.complete):
        ShippingAddress.objects.create(
            address = data['shipping']['address'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
            city = data['shipping']['city']
        )
    return JsonResponse('Form Data Received!',safe=False)

