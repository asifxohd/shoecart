from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from user_authentication.models import CustomUser
from cart.models import CartItem
from user_profile.models import Address
from .models import Orders,OrdersItem,CancelledOrderItem
from django.db import transaction
from datetime import timedelta 
from django.http import JsonResponse
from admin_home.models import SizeVariant
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
import razorpay
from payments.models import Wallet
from django.utils import timezone

# for the Razorpay
client = razorpay.Client(auth=('rzp_test_F83XKwHAQwFDZG', 'etDY4jG2xDLoFngOnDsM7wqY'))

# Create your views here.
def load_order_page(request):
    if 'user' in request.session:
        order_id = request.session['order_id']
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
        orders = Orders.objects.filter(user=user).order_by('order_date').exclude(payment_status="temp")
        order_items = OrdersItem.objects.filter(order__in=orders).order_by('order')

    return render(request, 'user_side/order_history.html', {'order_items':order_items})


# function for placing order 
def place_order(request):
    if 'user' in request.session:
        user_email = request.session['user']
        user_instance = CustomUser.objects.get(email=user_email)
        print("address_id")
        
        cart_items = CartItem.objects.filter(user=user_instance)
        for item in cart_items:
            if item.quantity > item.size_variant.quantity :
                print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                return JsonResponse({'empty' : True , 'message' : "Cart items Out of stock"})
        

        if request.method == 'POST':
            address_id = request.POST.get('address')
            payment_type = request.POST.get('payment')
            cart_items = CartItem.objects.filter(user=user_instance)
            print(payment_type)
            delivery_address = Address.objects.filter(id=address_id).first() 
                       
            if payment_type == "COD":
                if cart_items.exists():
                    try:
                        with transaction.atomic():
                            if 'final_amount' in request.session:
                                final_amount = int(request.session['final_amount'])
                            else:
                                total_amount = sum(cart_item.size_variant.price * cart_item.quantity for cart_item in cart_items)
                                
                            # Create a new order instance
                            order = Orders.objects.create(
                                user=user_instance,
                                address=delivery_address,
                                payment_method=payment_type,
                                quantity=0,
                                total_purchase_amount= final_amount if 'final_amount' in request.session else total_amount,

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

                            # Calculate the expected delivery date 
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
                
            # condition for the online peyment 
            elif payment_type == "onlinePayment":
                
                try:
                    if cart_items.exists():
                        if 'final_amount' in request.session:
                            final_amount = int(request.session['final_amount'])
                        else:
                            total_amount = sum(cart_item.size_variant.price * cart_item.quantity for cart_item in cart_items)
                                
                        # Create a new order instance
                        order = Orders.objects.create(
                            user=user_instance,
                            address=delivery_address,
                            payment_method=payment_type,
                            quantity=0,
                            payment_status="temp",
                            total_purchase_amount= final_amount if 'final_amount' in request.session else total_amount
 
                        )

                        request.session['order_id'] = str(order.order_id)
                        for cart_item in cart_items:
                            # Create an order item for each cart item
                            order_item = OrdersItem.objects.create(
                                order=order,
                                variant=cart_item.size_variant,
                                quantity=cart_item.quantity,
                                price=cart_item.size_variant.price,
                                status='Pending',
                            )

                        # Calculate the expected delivery date
                        order.expected_delivery_date = (order.order_date + timedelta(days=7))

                        order.save()
                       
                        amount_in_paise = final_amount if 'final_amount' in request.session else total_amount
                        print(amount_in_paise)
                       

                        # Create a Razorpay order
                        razorpay_order_data = {
                            'amount': amount_in_paise*100,
                            'currency': 'INR',
                            'receipt': str(order.order_id),
                        }

                        # Use the Razorpay client to create the order
                        razorpay_order = client.order.create(data=razorpay_order_data)
                        
                        return JsonResponse({'razorpay_order':razorpay_order, "success":False})

                    else:
                        response_data = {
                            'success': False,
                            'message': 'Your cart is empty',
                        }
                        return JsonResponse(response_data)

                except Exception as e:
                    print(f"Error while placing the order: {e}")
                    response_data = {
                        'success': False,
                        'message': 'Error while placing the order',
                    }
                    return JsonResponse(response_data)
            
            # condition for the walletpayment
            if payment_type == "wallet":
                
                if cart_items.exists():
                    if 'final_amount' in request.session:
                        final_amount = int(request.session['final_amount'])
                    else:
                        total_amount = sum(cart_item.size_variant.price * cart_item.quantity for cart_item in cart_items)
                        
                    try:
                        with transaction.atomic():
                            user_wallet = Wallet.objects.filter(user=user_instance).first()
                            last = user_wallet.balance
                            total_order_amount = sum(cart_item.size_variant.price * cart_item.quantity for cart_item in cart_items)

                            if user_wallet.balance >= total_order_amount:
                                order = Orders.objects.create(
                                    user=user_instance,
                                    address=delivery_address,
                                    payment_method=payment_type,
                                    quantity=0,
                                    payment_status="success",
                                    total_purchase_amount= final_amount if 'final_amount' in request.session else total_amount
                                )

                                for cart_item in cart_items:
                                    order_item = OrdersItem.objects.create(
                                        order=order,
                                        variant=cart_item.size_variant,
                                        quantity=cart_item.quantity,
                                        price=cart_item.size_variant.price,
                                        status='Order confirmed',
                                    )

                                    qua = cart_item.size_variant
                                    qua.quantity -= cart_item.quantity
                                    qua.save()

                                    order.quantity += order_item.quantity
                                    cart_item.delete()

                                order.expected_delivery_date = (order.order_date + timedelta(days=7))

                                

                                order.save()
                                request.session['order_id'] = str(order.order_id)
                                
                                
                                new = last - total_order_amount
                                
                                
                                p = Wallet(
                                    user=user_instance,
                                    transaction_details=f'Purchased for Rs.{total_order_amount}.00',
                                    transaction_type="Debit",
                                    balance=new,
                                    date=timezone.now(),
                                    transaction_amount=final_amount if 'final_amount' in request.session else total_amount
                                    
                                )
                                p.save()
                               
                                response_data = {
                                    'success': True,
                                    'message': 'Order placed successfully',
                                    'order_id': order.order_id,
                                    'insufficient_balance': False,
                                }
                            else:
                                response_data = {
                                    'success': False,
                                    'message': 'Insufficient balance in the wallet',
                                    'insufficient_balance': True,
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


def verifyPayment(request):
    email = request.session['user']
    user = CustomUser.objects.get(email=email)
    cart_items = CartItem.objects.filter(user=user)
    ord_id = request.session['order_id']
    order = Orders.objects.get(order_id=ord_id)
    order.payment_status = "success"
    order.save() 
    order_items = OrdersItem.objects.filter(order=order) 
    
    for order_item in order_items: 
        order_item.status = 'Order confirmed'
        order_item.save() 
        
        qua = order_item.variant
        qua.quantity -= order_item.quantity
        qua.save()

    cart_items.delete()  
    
    return JsonResponse({"success": True})

   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_orders(request):
    ite = OrdersItem.objects.exclude(order__payment_status="temp")
    items = ite.exclude(status="Cancellation request sent")
    print(items)
    return render(request,'admin_panel/admin_orders.html',{'items':items})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def view_order_details(request, id):
    obj = get_object_or_404(OrdersItem, id=id)

    try:
        cancelled_order_item = CancelledOrderItem.objects.get(order_item=id)
        reason = cancelled_order_item.cancellation_reason
    except CancelledOrderItem.DoesNotExist:
        reason = None

    return render(request, 'admin_panel/view_order_details.html', {'obj': obj, 'reason': reason})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def change_status(request,id):
    obj = OrdersItem.objects.get(id=id)
    status = request.POST.get('statusRadio')
    obj.status = status
    obj.save()
    return redirect('view_order_details',id=obj.id)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def cancel_request_page(request):
    order = OrdersItem.objects.filter(status="Cancellation request sent")
    return render(request, 'admin_panel/cancel_requests.html',{'order':order})


def cancel_request(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        cancel_reason = request.POST.get('cancel_reason')
        print(order_id)
        print(cancel_reason)

        order = OrdersItem.objects.filter(id=order_id).first()
        print(order)
        if order:
            order.status = "Cancellation request sent"
            order.save()

            cr = CancelledOrderItem.objects.create(order_item=order)
            cr.cancellation_reason = cancel_reason
            cr.save()
            response_data = {
                'success': True,
                'message': 'Cancellation request sent successfully',
                'order_status': order.status,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Order not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def cancell_product(request, id):
    email=request.session.get('user')
    user = CustomUser.objects.get(email=email)
    order =OrdersItem.objects.get(id=id)
    
    if order.order.payment_method == "COD":
        order.status = 'Cancelled'
        order.variant.quantity += order.quantity
        order.variant.save()
        order.save()
        return redirect('admin_orders')
    
    elif order.order.payment_method == "onlinePayment" or order.order.payment_method == "wallet":
        amount = order.price * order.quantity 
        user_wallet = Wallet.objects.filter(user=user).order_by("-id").first()
        
        if not user_wallet:
            balance = 0
        else:
            balance = user_wallet.balance
            
        new = balance + amount
        
        Wallet.objects.create(
            user=user,
            transaction_details=f'Order Cancelled Refund  Rs.{amount}.00',
            transaction_type = "Credit",
            transaction_amount = amount,
            balance = new
            
        )
        order.order.payment_status = "Refunded"
        order.order.save()
        order.status = 'Cancelled'
        order.save()
        return redirect('admin_orders')
    else:
        return redirect('admin_orders')
    
    
def return_product(request,id):
    
    email = request.session['user']
    user = CustomUser.objects.get(email=email)
    
    order = OrdersItem.objects.get(id=id)
    order.status = 'Returned'
    order.variant.quantity += order.quantity
    
    order.order.payment_status = "Refunded"
    order.order.save()
    
    amount = order.price
    wallet = Wallet.objects.filter(user=user).order_by('-id').first()
    
    if not wallet :
        balance = 0
    else:
        balance = wallet.balance
    
    new_balance = balance + amount
    
    Wallet.objects.create(
        user=user,
        transaction_amount=amount,
        transaction_type = "Credit",
        transaction_details = f'return Amount Rs.{amount} refunded',
        balance=new_balance,
    )
    order.save()
    order.variant.save()
    return redirect('order_history')
