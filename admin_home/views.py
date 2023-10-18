from django.shortcuts import render

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
    return render(request, "admin_panel/users.html")


