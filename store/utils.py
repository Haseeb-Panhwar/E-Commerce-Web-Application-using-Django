import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total':0,'get_cart_quantity':0,'shipping':False}
    cartitems = order['get_cart_quantity']
    for i in cart:
        try:
            cartitems+=cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            order['get_cart_total']+=total
            order['get_cart_quantity']+=cart[i]['quantity']
            
            item = {
                'product':{
                    'id':product.id,
                    'price':product.price,
                    'name':product.name,
                    'imageURL':product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
            if product.digital==False:
                order['shipping']=True
        except:
            pass
    return {'order':order,'cartitems':cartitems,'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_quantity
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartitems = cookieData['cartitems']

    return {'order':order,'cartitems':cartitems,'items':items}


def guestOrder(request,data):
    print("User not logged in!")
    print("Cookies: ",request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer , created = Customer.objects.get_or_create(email = email, name = name)
    order = Order.objects.create(customer=customer, complete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderitem = OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])
    return customer,order