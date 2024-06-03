from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import Product, Cart
from django.db.models import Count  
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from.models import Customer
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.

def home(request):
    return render(request,"app/home.html") 

def about(request):
    return render(request,"app/about.html") 

def contact(request):
    return render(request,"app/contact.html") 

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        print(title)
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(id = pk)

        return render(request, "app/productdetail.html",locals())

class CustomerRegistrationView(View):   
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistarion.html',locals())

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations user Registration is successful")
        else:
            messages.warning(request,"Invalid Input data")
        return render(request,'app/customerregistarion.html',locals())


class ProfileView(View):
    form = CustomerProfileForm()
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,
            zipcode=zipcode)

            reg.save()
            messages.success(request,"congratulation! profile is saved")

        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(id=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'app/updateaddress.html',locals())

    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add =   Customer.objects.get(id=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratrulations! Profile updated successfully")
        return render(request,'app/updateaddress.html',locals())

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user) 
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount+40

    return render(request, 'app/addtocart.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) 
        c.quantity+=1
        c.save()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount+40
        print(prod_id)
        data={
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)
