from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Product
from django.db.models import Count  
from .forms import CustomerRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User



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



                
       
