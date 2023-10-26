from django.shortcuts import render, redirect
from admin_home.models import Product,ProductImage
from .signals import contact_form_submitted
from admin_home.models import Category

# function for rendering baseuser
def baseuser(request):
    return render(request, 'user_side/base.html')

    
# function for loading product details in the landing page
def homepage(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related('productimage_set').filter(status=True)
        context = {
            "products":products,
            'cat':cat
        }
        return render(request, 'user_side/index.html', context)
    else:
        return redirect('signin')
    
    


#function for rendering the user profile page with the user details 
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "user_side/user_profile.html")
    else:
        return redirect('signin')
   


#function for rendering product page with products  
def product_page(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related('productimage_set').filter(status=True)
        context = {
            "products":products,
            'cat':cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')

# page for rendering men catogery shoe collection 
def products_men(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related('productimage_set').filter(gender='Male', status=True)
        context = {
            "products":products,
            'cat':cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')
    
    
#function for rendering the wome product details page 
def products_women(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related('productimage_set').filter(gender='Female', status=True)
        context = {
            "products":products,
            'cat':cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')
    
    
# product for the unisex page
def unisex(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related('productimage_set').filter(gender='Unisex', status=True)
        context = {
            "products":products,
            'cat':cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')
    
    
#function for rendring about page with the respective detals about the company 
def about(request):
    return render(request, 'user_side/about.html')


#function for rendering the page shoes 
def shoes(request):
    return render(request, 'user_side/products.html')


#fucntion for rendering the condact page    
def contact(request):
    if request.user.is_authenticated:
        success_message = None
        if request.method == 'POST':
            email = request.POST['email']
            message = request.POST['message']
            if email and message:
                contact_form_submitted.send(sender=request, email=email, message=message)
                success_message = 'Form submitted successfully'
                return render(request, 'user_side/contact.html',{'success_message': success_message})
            else:
                return redirect('contact')
    else:
        return redirect('signin')
     
    return render(request, 'user_side/contact.html')


#function for rendering product details with the product id 
def product_details(request, id):
    if request.user.is_authenticated:
        prod = Product.objects.get(id=id)
        product = Product.objects.filter(pk=id, status=True).prefetch_related('productimage_set', 'sizevariant_set').first()
        images = product.productimage_set.all()
        details = [product]  # Wrap the product in a list to pass it to the template as an iterable
    else:
        return redirect('signin')
    return render(request, "user_side/product_details.html", {'images': images, 'details': details})
