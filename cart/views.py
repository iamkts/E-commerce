from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart,Account,Order



def cartview(request):
    total=0
    u = request.user
    try:
        cart = Cart.objects.filter(user=u)
        for i in cart:
            total+=i.quantity*i.product.price
    except:
        pass
    return render(request, 'cart.html', {'c': cart,'total':total})


@login_required
# Create your views here.
def cart(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity < cart.product.stock):
            cart.quantity += 1
            cart.save()
    except:
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()

    return redirect('cart:cartview')

def cart_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity >1):
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except:
       pass

    return redirect('cart:cartview')
def full_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
    except:
       pass

    return cartview(request)
def orderform(request):
    if request.method=="POST":
        a=request.POST['a']
        ph = request.POST['ph']
        an = request.POST['an']

        u=request.user
        cart=Cart.objects.filter(user=u)
        total=0
        for i in cart:
            total+=i.quantity*i.product.price
        try:
            ac=Account.objects.get(acctnum=an)#to retrive the acctobject
            if ac.amount>= total:
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=ph,no_of_items=i.quantity,order_status="paid")
                    o.save()
                cart.delete()
                msg="Your order placed successfully"
                return render(request,"orderdetail.html",{'msg':msg})

            else:
                msg="insufficient amount,you can't place order"
                return render(request, "orderdetail.html", {'msg': msg})
        except:
            pass

    return render(request,'orderform.html')

# def orderform(request):
#     if (request.method == 'POST'):
#         a = request.POST['a']
#         ph = request.POST['ph']
#         an = request.POST['an']
#         u=request.user
#         cart=Cart.objects.filter(user=u)
#
#         total=0
#         for i in cart:
#             total+=i.quantity*i.product.price
#
#         try:
#
#             ac=Account.objects.get(acctnum=an)
#             if(ac.amount >= total):
#                 ac,amount=ac.amount-total
#                 ac.save()
#                 for i in cart:
#                     o=Order.objects.create(user=u,product=i.product,address=a,phone=ph,no_of_items=i.quantity,order_status="paid")
#                     o.save()
#                 cart.delete()
#                 msg="your order placed succesfully"
#                 return render(request,'orderdetail.html',{'msg': msg})
#             else:
#                 msg = "Insufficient amount cant place your order "
#                 return render(request, 'orderdetail.html', {'msg': msg})
#         except:
#             pass
#
#
#
#
#
#     return render(request, 'orderform.html')




def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o})