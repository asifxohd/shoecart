from django.shortcuts import render,redirect
from user_authentication.models import CustomUser
from admin_home.models import Category,Product,SizeVariant
from .forms import ProductForm
from django.db import transaction
from .forms import ProductForm, SizeVariantFormSet
from django.contrib import messages



# function for loading the Admin Base Template
def admin_base(request):
    return render(request, "admin_panel/admin_base.html")


# function for admin login
def admin_login(request):
    
    return render(request, "admin_panel/adminlogin.html")


#function for admin DashBoard
def admin_dash(request):
    
    return render(request, "admin_panel/admin_dash.html", )


# function to show products on the admin side 
def admin_products(request):
    products = Product.objects.all()
    return render(request, "admin_panel/products.html", {'products':products})


# function for showing the all users on the admin side
def admin_users(request):
    users = CustomUser.objects.all().exclude(is_superuser=True).order_by('id')
    return render(request, "admin_panel/users.html", {'users': users})


# function for showing all catogerys in the admin side 
def admin_catogory(request):
    catogory = Category.objects.all().order_by('id')
    return render(request, 'admin_panel/categories.html', {'categories':catogory})


#function for changing the user status (block and Unblock)
def user_status(request,id):
    user = CustomUser.objects.filter(id=id)[0]
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('admin_users')

 
# function for changing the catogery status (list and Unlist)
def category_status(request, id):
    cat = Category.objects.filter(id=id)[0]
    if cat.is_active == True:
        cat.is_active = False
        cat.save()
    else:
        cat.is_active = True
        cat.save()
    
    return redirect('admin_catogeory')



@transaction.atomic
def add_products(request):
    categories = Category.objects.all()
    sizes = ['41', '42', '43', '44', '45']

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        size_formset = SizeVariantFormSet(request.POST, prefix='size')
        size_index = 0  # Initialize a variable to keep track of the size index

        if product_form.is_valid() and size_formset.is_valid():
            # Save the product instance
            product = product_form.save()

            # Loop through size-quantity forms in the formset
            for size_form in size_formset:
                if size_form.cleaned_data:  # Check if the form is not empty
                    size_variant = size_form.save(commit=False)
                    size_variant.product = product
                    size_variant.size = sizes[size_index]  # Assign size from the list
                    size_variant.save()
                    print(f"Saved size variant for size {sizes[size_index]}")
                    size_index += 1  # Increment the size index

            print("Product saved successfully")
            messages.success(request, 'Product and size variants saved successfully.')
            return redirect('admin_products')
        else:
            messages.error(request, 'Error saving product and size variants. Please check the form.')
            print("Product form errors:", product_form.errors)
            print("Size variant formset errors:", size_formset.errors)
            print("POST data:", request.POST)
    else:
        product_form = ProductForm()
        size_formset = SizeVariantFormSet(prefix='size')

    return render(request, 'admin_panel/add_products.html', {'product_form': product_form, 'size_formset': size_formset, 'categories': categories, 'sizes': sizes})


# function for add catogory
def edit_category(request, id):
    category = Category.objects.filter(id=id)[0]
    if request.method == 'POST':
        updated_name = request.POST.get('category_name')
        category.name= updated_name
        category.save()
        return redirect('admin_catogeory')
        
    return render(request, 'admin_panel/editcat.html', {'category_name': category.name,})

# function for add catogery
def add_category(request):
    if request.method == 'POST':
        newCatogeryName = request.POST.get('new_updated_catogory')
        obj = Category(name=newCatogeryName)
        obj.save()
        return redirect('admin_catogeory')
    return render(request,'admin_panel/add_categories.html' )


# function for showing the product variant on the product variant page 
def show_product_varient(request, id):
    products = SizeVariant.objects.filter(product_id=id).prefetch_related('product')
    return render(request,'admin_panel/product_varient.html', {'products':products})   