from django.shortcuts import render, redirect
from admin_home.models import Product,ProductImage
from django.core.mail import send_mail
from django.http import JsonResponse


# function for rendering baseuser
def baseuser(request):
    return render(request, 'user_side/base.html')


# function for loading product details in the landing page
def homepage(request):
    products = Product.objects.prefetch_related('productimage_set').filter(status=True)
    return render(request, 'user_side/index.html', {'products': products})



#function for rendering the user profile page with the user details 
def user_profile(request):
    return render(request, "user_side/user_profile.html")


#function for rendering product page with products  
def product_page(request):
    return render(request, 'user_auth/product.html')


#function for rendring about page with the respective detals about the company 
def about(request):
    return render(request, 'user_auth/about.html')


#unction for rendering the page shoes 
def shoes(request):
    return render(request, 'user_auth/product.html')


#fucntion for rendering the condact page 
def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        if email and message:
            send_mail('Contact Form Submission', message, email, ['shoecartcalicut@gmail.com'])
            response_data = {'message': 'Form submitted successfully', 'status': 'success'}
        else:
            response_data = {'message': 'Invalid form submission', 'status': 'error'}
        return JsonResponse(response_data)

    return render(request, 'user_side/contact.html')



#function for rendering product details with the product id 
def product_details(request, id):
    product = Product.objects.filter(pk=id, status=True).prefetch_related('productimage_set', 'sizevariant_set').first()
    images = product.productimage_set.all()
    details = [product]  # Wrap the product in a list to pass it to the template as an iterable
    return render(request, "user_side/product_details.html", {'images': images, 'details': details})


