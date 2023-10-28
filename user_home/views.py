from django.shortcuts import render, redirect
from admin_home.models import Product, ProductImage
from .signals import contact_form_submitted
from admin_home.models import Category
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse



# function for rendering baseuser
def baseuser(request):
    return render(request, 'user_side/base.html')


# function for loading product details in the landing page
def homepage(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(status=True)
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/index.html', context)
    else:
        return redirect('signin')


# function for rendering the user profile page with the user details
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "user_side/user_profile.html")
    else:
        return redirect('signin')


# function for rendering product page with products
def product_page(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(status=True)
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')

# page for rendering men catogery shoe collection


def products_men(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(gender='Male', status=True)
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')


# function for rendering the wome product details page
def products_women(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(gender='Female', status=True)
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')


# product for the unisex page
def unisex(request):
    if request.user.is_authenticated:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(gender='Unisex', status=True)
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')


# function for rendring about page with the respective detals about the company
def about(request):
    return render(request, 'user_side/about.html')


# function for rendering the page shoes
def shoes(request):
    return render(request, 'user_side/products.html')


# fucntion for rendering the condact page
def contact(request):
    if request.user.is_authenticated:
        success_message = None
        if request.method == 'POST':
            email = request.POST['email']
            message = request.POST['message']
            if email and message:
                contact_form_submitted.send(
                    sender=request, email=email, message=message)
                success_message = 'Form submitted successfully'
                return render(request, 'user_side/contact.html', {'success_message': success_message})
            else:
                return redirect('contact')
    else:
        return redirect('signin')

    return render(request, 'user_side/contact.html')


# function for rendering product details with the product id
def product_details(request, id):
    if request.user.is_authenticated:
        prod = Product.objects.get(id=id)
        product = Product.objects.filter(pk=id, status=True).prefetch_related(
            'productimage_set', 'sizevariant_set').first()
        images = product.productimage_set.all()
        # Wrap the product in a list to pass it to the template as an iterable
        details = [product]
    else:
        return redirect('signin')
    return render(request, "user_side/product_details.html", {'images': images, 'details': details})


# funtion for chatogery filter
def show_category(request, id):
    cat = Category.objects.filter(is_active=True)
    products = Product.objects.filter(status=True, category_id=id)
    return render(request, 'user_side/products.html',{'cat': cat, 'products': products})


# function for filtering by price
def show_price_filtering(request):
    products = Product.objects.filter(status=True)
    sort_order = request.GET.get('sort', 'default')
    cat = Category.objects.filter(is_active=True)
    if sort_order == 'popularity':
        pass
    elif sort_order == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_order == 'price_high_to_low':
        products = products.order_by('-price')
        
    return render(request,'user_side/products.html',{'cat': cat, 'products': products} )

# function for the showing the products between the price range on the user interface
def show_price_between(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    cat = Category.objects.filter(is_active=True)
    products = Product.objects.filter(price__gte=min_price, price__lte=max_price, status=True)

    return render(request, 'user_side/products.html', {'products': products, 'cat': cat})


# function for auto compleat searching products 
def autocompleat(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for i in qs:
            names.append(i.name)
        return JsonResponse(names, safe=False)
    return render(request, 'user_side/products.html')
