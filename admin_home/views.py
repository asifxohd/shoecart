from django.shortcuts import render,redirect
from user_authentication.models import CustomUser
from admin_home.models import Category,Product,SizeVariant
from .forms import ProductForm


# function for loading the Admin Base Template
def admin_base(request):
    return render(request, "admin_panel/admin_base.html")


# function for admin login
def admin_login(request):
    return render(request, "admin_panel/adminlogin.html")


#function for admin DashBoard
def admin_dash(request):
    return render(request, "admin_panel/admin_dash.html")


# function to show products on the admin side 
def admin_products(request):
    return render(request, "admin_panel/products.html")


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


def add_products(request):
    categories = Category.objects.all()
    sizes = ['41', '42', '43', '44', '45']

    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new product instance, but don't save it yet
            product = form.save(commit=False)

            # Handle size and quantity
            size = request.POST.get('size')
            quantity = request.POST.get('quantity')

            if size and size in sizes and quantity:
                product.save()  # Save the product

                # Create a new SizeVariant instance
                SizeVariant.objects.create(product=product, size=size, quantity=quantity)
            else:
                return render(request, 'admin_panel/add_products.html', {'form': form, 'categories': categories, 'sizes': sizes, 'error_message': 'Invalid size or quantity'})

            # Redirect to a success page or any other page
            return redirect('admin_products')
        else:
             print(form.errors)

    else:
        form = ProductForm()

    return render(request, 'admin_panel/add_products.html', {'form': form, 'categories': categories, 'sizes': sizes})



        
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
