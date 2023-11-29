from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from user_authentication.models import CustomUser
from .models import CartItem,Wishlist
from admin_home.models import SizeVariant,Product
from django.utils import timezone
from django.http import HttpResponse
from user_profile.models import Address
from django.views.decorators.cache import cache_control
from datetime import date
from coupons.models import Coupons
# Create your views here.


#function for rendering cart page with cart details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
            if (CartItem.objects.filter(user=user , size_variant=variant_size)):
                return JsonResponse({'status' : "Product already in cart"})
            else:
                CartItem.objects.create(user=user, size_variant=variant_size,created_at=timezone.now(),cart_price=variant_size.price)
                cart_count_ajax = CartItem.objects.filter(user=user).count()
            return JsonResponse({'status' : "Product added successfully",'success':True ,'cart_count_ajax' : cart_count_ajax})

        else:
            return redirect('signin')
    else:
        return render(request,'user_side/index.html')
    

#function for removing the item from cart
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_item_from_cart(request):
    if 'user' in request.session:
        if request.method == 'POST':
            user_emil = request.session['user']
            user = CustomUser.objects.filter(email=user_emil).first()
            item_id = request.POST.get('item_id') 
            try:
                cart_item = CartItem.objects.get(id=item_id)
                cart_item.delete()
                cart_count = CartItem.objects.filter(user=user).count()
                return JsonResponse({'cartCount': cart_count, 'message': 'Item removed successfully'})
            except CartItem.DoesNotExist:
                return JsonResponse({'message': 'Item not found'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)
    else:
        return redirect('signin')
    
    
#function for updating the cart details like price, quantity and other info 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
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
                    cart.quantity += 1
                    cart.save()           
            else:
                if cart.quantity > 1:
                    cart.quantity -= 1
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request):
    if 'user' in request.session:
        user = request.session['user']
        userr = CustomUser.objects.get(email=user) 
        addresses = Address.objects.filter(user=userr.id, is_listed=True)
        obj = CartItem.objects.filter(user=userr)
        total = sum(obj.values_list('cart_price', flat=True))
        coupons = Coupons.objects.filter(active=True, valid_to__gte=date.today()).order_by('-id')
        print(coupons)
        
    return render(request, 'user_side/checkout.html', {'addresses': addresses, 'obj':obj, 'total':total,'coupons':coupons})


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


def wishlist(request):
    if 'user' in request.session:
        user = get_object_or_404(CustomUser, email=request.session['user'])
        
        wishlist_products = Wishlist.objects.filter(user=user)
        product_ids = [wishlist.product_id for wishlist in wishlist_products]

        products = Product.objects.prefetch_related('productimage_set', 'sizevariant_set').filter(id__in=product_ids)

        for product in products:
            first_variant = product.sizevariant_set.first()
            product.first_variant_price = first_variant.price if first_variant else None

        context = {
            "products": products,
        }
        
        return render(request, 'user_side/wishlist.html', context)

    return HttpResponse("User not logged in")


def add_to_wishlist(request):
    if request.method == 'POST':
        if 'user' in request.session:
            email = request.session['user']
            user = CustomUser.objects.get(email=email)

            try:
                product_id = int(request.POST.get('productId'))
                product = Product.objects.get(id=product_id)

                if Wishlist.objects.filter(user=user, product=product).exists():
                    return JsonResponse({'success': False, 'message': 'Already in wishlist'})

                Wishlist.objects.create(user=user, product=product)
                wishlist_count = Wishlist.objects.filter(user=user).count()

                return JsonResponse({'success': True, 'wishlist_count': wishlist_count})

            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Product not found'})
                
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_wishlist(request):
    print("Removing Wishlist")

    if 'user' in request.session:
        print("Removing Wishlist")
        if request.method == 'POST':
            user = get_object_or_404(CustomUser, email=request.session['user'])
            prod_id = request.POST.get('product_id')
            wishlist_item = get_object_or_404(Wishlist, user=user, product_id=prod_id)
            wishlist_item.delete()
            response_data = {'success': True, 'message': 'Product removed from wishlist successfully'}
            return JsonResponse(response_data)

    response_data = {'success': False, 'message': 'Invalid request'}
    return JsonResponse(response_data)