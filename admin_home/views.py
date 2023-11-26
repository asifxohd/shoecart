from django.shortcuts import render, redirect
from user_authentication.models import CustomUser
from admin_home.models import Category, Product, SizeVariant, ProductImage,Banner
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login
from orders.models import Orders, OrdersItem
from datetime import datetime,timedelta


# function for loading the Admin Base Template
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_base(request):
    return render(request, "admin_panel/admin_base.html")


# function for admin login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                request.session['admin'] = email
                return redirect('admin_dashboard')
            else:
                messages.error(request, "User has No access to Admin panel")
                return redirect('admin_login')
        else:
            messages.error(request, "Invalid user")
            return redirect('admin_login')
    return render(request, 'admin_panel/admin_login.html')


# function for showing the all users on the admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_users(request):
    users = CustomUser.objects.all().exclude(is_superuser=True).order_by('id')
    return render(request, "admin_panel/users.html", {'users': users})


# function for showing all catogerys in the admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_catogory(request):
    catogory = Category.objects.all().order_by('id')
    return render(request, 'admin_panel/categories.html', {'categories': catogory})


# function for changing the user status (block and Unblock)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def user_status(request, id):
    user = CustomUser.objects.filter(id=id)[0]
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('admin_users')


# function for changing the catogery status (list and Unlist)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def category_status(request, id):
    cat = Category.objects.filter(id=id)[0]
    if cat.is_active == True:
        cat.is_active = False
        cat.save()
    else:
        cat.is_active = True
        cat.save()

    return redirect('admin_catogeory')


# function for adding product data like image ,size variants,etc.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def add_products(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category_id = request.POST['category']
        gender = request.POST['gender']

        product = Product(
            name=name,
            description=description,
            category_id=category_id,
            gender=gender,
        )

        product.save()
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage(product=product, image=image).save()
        return redirect('admin_products')

    return render(request, 'admin_panel/add_products.html', {'categories': categories})


# function for edit catogory
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def edit_category(request, id):
    category = Category.objects.get(id=id)

    if request.method == 'POST':
        updated_name = request.POST.get('category_name')
        print(updated_name)

        if updated_name != category.name:
            if Category.objects.filter(name=updated_name).exists():
                messages.error(
                    request, "Category with this name already exists")
            else:
                category.name = updated_name
                category.save()
                return redirect('admin_catogeory')

    return render(request, 'admin_panel/editcat.html', {'category_name': category.name})


# function for add catogery
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def add_category(request):
    if request.method == 'POST':
        newCatogeryName = request.POST.get('new_updated_catogory')
        if Category.objects.filter(name=newCatogeryName):
            messages.error(request, "Category already exists")
            return redirect('add_category')

        obj = Category(name=newCatogeryName)
        obj.save()
        return redirect('admin_catogeory')
    return render(request, 'admin_panel/add_categories.html')


# function for showing the product variant, image on the product variant page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def show_product_varient(request, id):
    product = Product.objects.filter(pk=id, status=True).prefetch_related(
        'productimage_set', 'sizevariant_set').first()
    print(product)
    return render(request, 'admin_panel/product_varient.html', {'product': product})


# function for showing the product on trash page variant, image on the product variant page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def trash_product_varient(request, id):
    product = Product.objects.filter(pk=id, status=False).prefetch_related(
        'productimage_set', 'sizevariant_set').first()
    print(product)
    return render(request, 'admin_panel/product_varient.html', {'product': product})


# function to show products on the admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_products(request):
    products = Product.objects.prefetch_related(
        'productimage_set').filter(status=True)
    return render(request, "admin_panel/products.html", {'products': products})


# function for soft-deleting the product
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def ajax_soft_delete_product(request, id):
    product = Product.objects.filter(id=id).first()
    if product:
        product.status = False
        product.save()
        return redirect('admin_products')
    else:
        return redirect('admin_products')


# function for loading the product Trash coloumn
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_trash(request):
    products = Product.objects.prefetch_related(
        'productimage_set').filter(status=False)
    return render(request, "admin_panel/trash.html", {'products': products})


# function for restoring product from the product Trash
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def restore_product(request, id):
    product = Product.objects.filter(id=id).first()
    if product:
        product.status = True
        product.save()
        return render(request, "admin_panel/trash.html")
    else:
        return redirect('admin_trash')


# function for editing the product details and sending the context for the input fields
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def edit_product(request, id):
    product = Product.objects.get(id=id)
    images = ProductImage.objects.filter(product=product)
    size_variants = SizeVariant.objects.filter(product=product)
    cat = Category.objects.all()

    context = {
        'cat': cat,
        'product': product,
        'images': images,
        'size_variants': size_variants,
    }

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.category_id = request.POST['category']
        product.gender = request.POST['gender']
        product.save()

        
        new_images = request.FILES.getlist('images')

        if new_images:
            ProductImage.objects.filter(product=product).delete()
            for image in new_images:
                ProductImage(product=product, image=image).save()

        print("Product updated successfully")

        return redirect('admin_products')

    return render(request, 'admin_panel/edit_products.html', context)


# function for adding the product variant
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def add_variand(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        size = request.POST['size']
        quantity = request.POST['quantity']
        price = request.POST['price']
        discount_percent = request.POST['discount_percent']

        variand = SizeVariant(
            product=product,
            size=size,
            quantity=quantity,
            price=price,
            discount_percent=discount_percent

        )
        variand.save()
        
        return redirect('product_varient', id=id)

    return render(request, 'admin_panel/add_variand.html')


# function for edit varint
def edit_variand(request, id):
    var = SizeVariant.objects.filter(pk=id).first()
    
    if request.method == 'POST':
        quantity = request.POST['quantity']
        price = request.POST['price']
        discount_percent = request.POST['discount_percent']
        
        var.quantity=quantity
        var.price=price
        var.discount_percent=discount_percent
        
        var.save()
        
        return redirect('product_varient',id=var.product.id)
        
      
    return render(request,'admin_panel/edit_variand.html', {'var':var})


# function for rendering the admin side banner page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_banner(request):
    
    return render(request, 'admin_panel/admin_banners.html')



# function for adding new banners 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def add_banner(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        main_title = request.POST.get('mainTitleInput')
        subtitle = request.POST.get('subtitleInput')
        file_input = request.FILES.get('fileInput')
        banner_type = request.POST.get('bannerTypeSelect')
        print(file_input)

        # Save the banner to the database
        banner = Banner(
            main_title=main_title,
            subtitle=subtitle,
            file_input=file_input,
            banner_type=banner_type,
        )
        banner.save()

        return redirect('banner_page')  
    return render(request, 'admin_panel/main_banner.html')


# function for rendering the admin side sales report page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_sales(request):
    delivered_orders = Orders.objects.filter(payment_status='success').order_by('-order_date').distinct()
    print(delivered_orders)
    

    context = {
        'recent_orders': delivered_orders
    }


    return render(request, 'admin_panel/sales_report.html', context)

