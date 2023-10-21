from django.shortcuts import render
from admin_home.models import Product,ProductImage

# Create your views here.
def baseuser(request):
    return render(request, 'user_side/base.html')

def homepage(request):
    products = Product.objects.all()
    return render(request, 'user_side/index.html', {'products':products})

def product_page(request):
    return render(request, 'user_auth/product.html')

def about(request):
    return render(request, 'user_auth/about.html')

def shoes(request):
    return render(request, 'user_auth/product.html')

def contact(request):
    return render(request, 'user_auth/contact.html')

def product_details(request, id):
    details = Product.objects.filter(id=id)
    images = ProductImage.objects.filter(product=details)
    return render(request, "user_side/product_details.html",{'images':images},{'details':details})

