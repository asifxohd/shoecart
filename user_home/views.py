from django.shortcuts import render, redirect
from admin_home.models import Product,Banner,Category,SizeVariant
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from user_home.models import Contact
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.db.models import Max
from django.db.models import OuterRef, Subquery



# function for rendering baseuser
def baseuser(request):
    return render(request, 'user_side/base.html')

def homepage(request):
    if 'user' in request.session:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set', 'sizevariant_set'
        ).filter(status=True)[:8]
        
        for product in products:
            first_variant = product.sizevariant_set.first()
            product.first_variant_price = first_variant.price if first_variant else None
            
        ban1 = Banner.objects.filter(banner_type="main_banner",is_active=True).first()
        ban2 = Banner.objects.filter(banner_type="mini_banner_left",is_active=True).first()
        ban3 = Banner.objects.filter(banner_type="mini_banner_center",is_active=True).first()
        ban4 = Banner.objects.filter(banner_type="mini_banner_right",is_active=True).first()
        context = {
            "products": products,
            'cat': cat,
            'ban1':ban1,
            'ban2':ban2,
            'ban3':ban3,
            'ban4':ban4
        }
        
        return render(request, 'user_side/index.html', context)
    else:
        return redirect('signin')


# function for rendering product page with products
def product_page(request):
    if 'user' in request.session:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(status=True)
        
        for product in products:
            first_variant = product.sizevariant_set.first()
            product.first_variant_price = first_variant.price if first_variant else None

        paginator = Paginator(products,12)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        page_count = page_obj.paginator.num_pages
        context = {
            "products": page_obj,
            'cat': cat,
            'page_count':range(page_count)
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')


# page for rendering men catogery shoe collection
def products_men(request):
    if 'user' in request.session:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(gender='Male', status=True)
        
        for product in products:
            first_variant = product.sizevariant_set.first()
            product.first_variant_price = first_variant.price if first_variant else None
        
        paginator = Paginator(products,12)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        page_count = page_obj.paginator.num_pages
            
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')


# function for rendering the wome product details page
def products_women(request):
    if 'user' in request.session:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(gender='Female', status=True)
        
        for product in products:
            first_variant = product.sizevariant_set.first()
            product.first_variant_price = first_variant.price if first_variant else None
            
        context = {
            "products": products,
            'cat': cat
        }
        return render(request, 'user_side/products.html', context)
    else:
        return redirect('signin')


# product for the unisex page
def unisex(request):
    if 'user' in request.session:
        cat = Category.objects.filter(is_active=True)
        products = Product.objects.prefetch_related(
            'productimage_set').filter(gender='Unisex', status=True)
        
        for product in products:
            first_variant = product.sizevariant_set.first()
            product.first_variant_price = first_variant.price if first_variant else None
            
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
    if 'user' in request.session:
        if request.method == 'POST':
            email = request.POST['email']
            message = request.POST['message']
            Contact.objects.create(email=email, message=message)
            return redirect('contact')
    else:
        return redirect('signin')

    return render(request, 'user_side/contact.html')


# function for rendering product details with the product id
def product_details(request, id):
    if 'user' in request.session:
        k=product = Product.objects.filter(pk=id, status=True).prefetch_related(
            'productimage_set', 'sizevariant_set').first()
        sizes = SizeVariant.objects.filter(product=product).order_by('size')
        images = product.productimage_set.all()

        # Check if the product has variants and get the first one
        # first_variant = None
        # if product.sizevariant_set.exists():
        first_variant = product.sizevariant_set.first()

        return render(request, "user_side/product_details.html", {'images': images, 'variant': first_variant,'k':k ,'sizes':sizes})
    else:
        return redirect('signin')



def get_variant_details(request, variant_id):
    size_variant = get_object_or_404(SizeVariant, id=variant_id)

    # Create a dictionary with the details you want to return
    variant_details = {
        'price': size_variant.price,
        'discount_percent':size_variant.discount_percent,
        'quantity': size_variant.quantity
    }

    return JsonResponse(variant_details)

# funtion for chatogery filter
def show_category(request, id):
    cat = Category.objects.filter(is_active=True)
    products = Product.objects.filter(status=True, category_id=id)
    
    for product in products:
        first_variant = product.sizevariant_set.first()
        product.first_variant_price = first_variant.price if first_variant else None
            
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
    sort_by = request.GET.get('sort_by', 'default')

    try:
        min_price = float(min_price)
        max_price = float(max_price)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid min_price or max_price")

    cat = Category.objects.filter(is_active=True)

    product_ids = SizeVariant.objects.filter(price__gte=min_price, price__lte=max_price).values('product').annotate(max_price=Max('price')).values_list('product', flat=True)

    products = Product.objects.filter(id__in=product_ids, status=True)

    for product in products:
        first_variant = product.sizevariant_set.first()
        product.first_variant_price = first_variant.price if first_variant else None

    return render(request, 'user_side/products.html', {'products': products, 'cat': cat, 'sort_by': sort_by})


# function for search
def search(request):
    search_query = request.GET['search-product']
    products_match = Product.objects.filter(name__icontains=search_query)
    for product in products_match:
        first_variant = product.sizevariant_set.first()
        product.first_variant_price = first_variant.price if first_variant else None
   
    return render(request, "user_side/products.html" , {'products': products_match})



def sorting_products(request):
    sort_by = request.GET.get('sort_by', 'default')

    cat = Category.objects.filter(is_active=True)

    # Subquery to get the latest size variant for each product
    latest_size_variant = SizeVariant.objects.filter(
        product=OuterRef('pk')
    ).order_by('-id').values('price')[:1]

    if sort_by == 'low_to_high':
        products = Product.objects.filter(status=True).annotate(
            first_variant_price=Subquery(latest_size_variant)
        ).order_by('first_variant_price')
    elif sort_by == 'high_to_low':
        products = Product.objects.filter(status=True).annotate(
            first_variant_price=Subquery(latest_size_variant)
        ).order_by('-first_variant_price')
    else:
        products = Product.objects.filter(status=True)

    context = {
        'products': products,
        'cat':cat
    }

    return render(request, "user_side/products.html", context)
