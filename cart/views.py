from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from user_authentication.models import CustomUser
from .models import CartItem
from admin_home.models import SizeVariant,Product
from django.utils import timezone
from django.http import HttpResponse
# Create your views here.


#function for rendering cart page with cart details
def cart_page(request):
    email = request.session.get('user')
    if email:
        user = get_object_or_404(CustomUser, email=email)
        cart_items = CartItem.objects.filter(user=user).order_by('id')
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
            print(variant_id)
            variant_size = SizeVariant.objects.get(id=variant_id)
            
            if (CartItem.objects.filter(user=user , size_variant=variant_size)):
                return JsonResponse({'status' : "Product already in cart"})
            else:
                CartItem.objects.create(user=user, size_variant=variant_size,created_at=timezone.now())
            return JsonResponse({'status' : "Product added successfully",'success':True})

        else:
            return redirect('signin')
    else:
        return render(request,'user_side/index.html')
    

#function for removing the item from cart
def remove_item_from_cart(request):
    if 'user' in request.session:
        if request.method == 'POST':
            item_id = request.POST.get('item_id') 
            try:
                cart_item = CartItem.objects.get(id=item_id)
                cart_item.delete()
                return JsonResponse({'message': 'Item removed successfully'})
            except CartItem.DoesNotExist:
                return JsonResponse({'message': 'Item not found'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)
    else:
        return redirect('signin')
    
    
#function for updating the cart details like price, quantity and other info    
def update_cart(request):
    if request.method == 'POST':
        if 'user' in request.session:
            user_emil = request.session['user']
            user = CustomUser.objects.filter(email=user_emil).first()
            change = int(request.POST.get('change'))
            variant_id = request.POST.get('variantId')
            variant_instence = SizeVariant.objects.get(id=variant_id)
            quantity = request.POST.get('quantity')          
            cart = CartItem.objects.get(user=user, size_variant=variant_instence)
            
            if change == 1:
                cart.quantity += 1
                cart.save()
            else:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart.quantity = 1
            
            
            print(type(change))
        response_data = {'updatedQuantity': cart.quantity}
        return JsonResponse(response_data)

    return HttpResponse(status=200)
