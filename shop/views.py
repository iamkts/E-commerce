from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from shop.models import Category,Product
# Create your views here.
def allcategories(request):
    c = Category.objects.all()
    return render(request, 'category.html',{'c':c})

def productdetail(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request,'productdetail.html',{'c':c,'p':p})
def detail(request, p):
    p = Product.objects.get( name=p)
    return render(request, 'detail.html', {'p': p})

def user_login(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def register(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        c = request.POST['c']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']
        # pl = request.POST['pl']
        # num = request.POST['num']
        if (p == c):
            b = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            b.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Passwords are not same")
    return render(request, 'register.html')

@login_required
def user_logout(request):
    logout(request)
    return user_login(request)

