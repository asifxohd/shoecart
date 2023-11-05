from django.shortcuts import render,redirect,get_list_or_404
from django.http import HttpResponse
from user_authentication.models import CustomUser
from cart.models import CartItem
from user_profile.models import Address
from .models import Orders,OrdersItem
from django.db import transaction
from datetime import timedelta 
from django.http import JsonResponse
from admin_home.models import SizeVariant
import uuid
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control



# Create your views here.
def load_order_page(request):
    if 'user' in request.session:
        order_id = uuid.UUID(request.session['order_id'])
        current_order = Orders.objects.get(order_id=order_id)
        context= {
        "current_order" : current_order
        }
        
    return render(request, 'user_side/order_details.html',context)

#function for loading order history
def order_history(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        orders = Orders.objects.filter(user=user)
        order_items = OrdersItem.objects.filter(order__in=orders)

    return render(request, 'user_side/order_history.html', {'order_items':order_items})


def place_order(request):
    if 'user' in request.session:
        user_email = request.session['user']
        user_instance = CustomUser.objects.get(email=user_email)

        if request.method == 'POST':
            address_id = request.POST.get('selected_address')
            payment_type = request.POST.get('payment')
            delivery_address = Address.objects.filter(id=address_id).first()

            cart_items = CartItem.objects.filter(user=user_instance)
            if cart_items.exists():
                try:
                    with transaction.atomic():
                        # Create a new order instance
                        order = Orders.objects.create(
                            user=user_instance,
                            address=delivery_address,
                            payment_method=payment_type,
                            quantity=0,
                        )

                        for cart_item in cart_items:
                            # Create an order item for each cart item
                            order_item = OrdersItem.objects.create(
                                order=order,
                                variant=cart_item.size_variant,
                                quantity=cart_item.quantity,
                                price=cart_item.size_variant.price,
                                status='Order confirmed',
                            )
                            
                            #for dicreamenting quantity
                            qua  = cart_item.size_variant
                            qua.quantity -= cart_item.quantity
                            qua.save()
                            
                            
                            # Update the order's price, total_amount, and quantity
                            order.quantity += order_item.quantity

                            cart_item.delete()

                        # Calculate the expected delivery date (you can customize this logic)
                        # For example, add some days to the current date
                        order.expected_delivery_date = (order.order_date + timedelta(days=7))

                        # Save the order
                        order.save()
                        request.session['order_id'] = str(order.order_id)
                       

                        response_data = {
                            'success': True,
                            'message': 'Order placed successfully',
                            'order_id': order.order_id,
                        }
                        return JsonResponse(response_data)

                except Exception as e:
                    print(f"Error while placing the order: {e}")
                    response_data = {
                        'success': False,
                        'message': 'Error while placing the order',
                    }
                    return JsonResponse(response_data)

            else:
                response_data = {
                    'success': False,
                    'message': 'Your cart is empty',
                }
                return JsonResponse(response_data)

    else:
        response_data = {
            'success': False,
            'message': 'User not logged in',
        }
        return JsonResponse(response_data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_orders(request):
    items = OrdersItem.objects.all()
    print(items)
    return render(request,'admin_panel/admin_orders.html',{'items':items})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def view_order_details(request, id):
    obj = OrdersItem.objects.get(id=id)
    print(obj)
    return render(request,'admin_panel/view_order_details.html',{'obj':obj})