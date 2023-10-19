from django.shortcuts import render,redirect
from user_authentication.models import CustomUser

# Create your views here.
def admin_base(request):
    return render(request, "admin_panel/admin_base.html")

def admin_login(request):
    return render(request, "admin_panel/adminlogin.html")

def admin_dash(request):
    return render(request, "admin_panel/admin_dash.html")

def admin_products(request):
    return render(request, "admin_panel/products.html")

def admin_users(request):
    users = CustomUser.objects.all().exclude(is_superuser=True).order_by('id')
    
    return render(request, "admin_panel/users.html", {'users': users})

def admin_catogory(request):
    return render(request, 'admin_panel/categories.html')

def user_status(request,id):
    user = CustomUser.objects.filter(id=id)[0]
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('admin_users')

def add_products(request):
    return render(request,'admin_panel/add_products.html')
        
    
    

