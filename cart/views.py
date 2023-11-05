from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from user_authentication.models import CustomUser
from .models import CartItem
from admin_home.models import SizeVariant,Product
from django.utils import timezone
from django.http import HttpResponse
from user_profile.models import Address
# Create your views here.


#function for rendering cart page with cart details
def cart_page(request):
    email = request.session.get('user')
    if email:
        user = get_object_or_404(CustomUser, email=email)
        cart_items = CartItem.objects.filter(user=user).order_by('id')  
        subPrice = sum(cart_items.values_list('cart_price', flat=True))
        return render(request, 'user_side/shoping_cart.html', {'cart_items': cart_items, 'subPrice':subPrice})
    else:
        return redirect('signin')
        
#function for adding the product variant to the cart table 
def add_to_cart(request):
    if request.method == 'POST':
        if 'user' in request.session:

            email = request.session['user']
            user = CustomUser.objects.get(email=email)
            variant_id = request.POST.get('variantId')
            variant_size = SizeVariant.objects.get(id=variant_id)
            print(variant_size.price)
            if (CartItem.objects.filter(user=user , size_variant=variant_size)):
                return JsonResponse({'status' : "Product already in cart"})
            else:
                CartItem.objects.create(user=user, size_variant=variant_size,created_at=timezone.now(),cart_price=variant_size.price)
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
            cart = CartItem.objects.get(user=user, size_variant=variant_instence)
            print(variant_instence.quantity)
            if change == 1:
                if variant_instence.quantity > cart.quantity:
                    if cart.quantity < 10:
                        cart.quantity += 1
                        cart.save()
                    else:
                        cart.quantity = 10
                        cart.save()
                else:
                    pass
            else:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart.quantity = 1
                    cart.save()
            
            # for showing total price of the each product 
            priceOfInstence = variant_instence.price
            total = cart.quantity * priceOfInstence
            cart.cart_price = total
            cart.save()
            
            # for showing the subtotal
            userCart = CartItem.objects.filter(user=user)
            subTotal = sum(userCart.values_list('cart_price', flat=True))
            
        response_data = {'updatedQuantity': cart.quantity, 'total':total, 'subTotal':subTotal}
        return JsonResponse(response_data)
    else:
        return redirect('signin')


def checkout(request):
    if 'user' in request.session:
        user = request.session['user']
        userr = CustomUser.objects.get(email=user) 
        addresses = Address.objects.filter(user=userr.id, is_listed=True)
        obj = CartItem.objects.filter(user=userr)
        total = sum(obj.values_list('cart_price', flat=True))
        
    return render(request, 'user_side/checkout.html', {'addresses': addresses, 'obj':obj, 'total':total})


def checkout_add_address(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pin_code')
        landmark = request.POST.get('land_mark')

        new_address = Address(

            user=user,
            full_name=full_name,
            mobile_number=mobile_number,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            landmark=landmark
        )
        new_address.save()

        return redirect('checkout')
    else:
        return redirect('signin')
    
    
def checkout_update_address(request, id):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        address = Address.objects.get(id=id)
        print(address)
        if request.method == 'POST':
            
            full_name = request.POST.get('full_name')
            mobile_number = request.POST.get('mobile_number')
            address_line = request.POST.get('address_line')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pin_code')
            landmark = request.POST.get('land_mark')
            
            address.full_name = full_name
            address.mobile_number = mobile_number
            address.address_line = address_line
            address.city = city
            address.state = state
            address.pincode = pincode
            address.landmark = landmark
            
            address.save()
                
            return redirect('checkout')
    
    return render(request,'user_side/check_update.html', {'address':address})

def checkout_address(request):
    return render(request,'user_side/checkout_address.html')