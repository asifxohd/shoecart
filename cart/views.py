from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from user_authentication.models import CustomUser
from .models import CartItem
from admin_home.models import SizeVariant,Product
from django.utils import timezone
# Create your views here.


#function for rendering cart page with cart details
def cart_page(request):
    email = request.session.get('user')
    if email:
        user = get_object_or_404(CustomUser, email=email)
        cart_items = CartItem.objects.filter(user=user)
        print(cart_items)
        return render(request, 'user_side/shoping_cart.html', {'cart_items': cart_items})
    else:
        return redirect('signin')
        
#function for adding the product variant to the cart table 
def add_to_cart(request):
    if request.method == 'POST':
        if 'user' in request.session:

            email = request.session['user']
            user = CustomUser.objects.get(email=email)
            variant_id = request.POST.get('variantId')
            product_id = SizeVariant.objects.filter(id=variant_id).first().product.pk
            prod = Product.objects.get(id=product_id)
            variant_size = SizeVariant.objects.get(id=variant_id)
            
            if (CartItem.objects.filter(user=user , product=prod)):
                return JsonResponse({'status' : "Product already in cart"})
            else:
                CartItem.objects.create(user=user,product=prod,size_variant=variant_size,created_at=timezone.now())
            return JsonResponse({'status' : "Product added successfully"})

        else:
            return redirect('signin')
    else:
        return render(request,'user_side/index.html')
    
