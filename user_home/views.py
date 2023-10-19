from django.shortcuts import render

# Create your views here.
def baseuser(request):
    return render(request, 'user_side/base.html')

def homepage(request):
    return render(request, 'user_side/index.html')

def product_page(request):
    return render(request, 'user_auth/product.html')

def about(request):
    return render(request, 'user_auth/about.html')

def shoes(request):
    return render(request, 'user_auth/product.html')

def contact(request):
    return render(request, 'user_auth/contact.html')

def product_details(request):
    return render(request, "user_side/product_details.html")

