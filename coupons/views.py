from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from .models import Coupons,CouponUsage
from django.utils import timezone
from django.http import JsonResponse
from user_authentication.models import CustomUser
from cart.models import CartItem


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def render_coupons(request):
    coupons = Coupons.objects.all().order_by('-id')
    return render(request,"admin_panel/coupons.html",{"coupons": coupons})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def add_coupons(request):
    if request.method == 'POST':
        coupon_title = request.POST.get('coupon_title')
        coupon_code = request.POST.get('coupon_code')
        discount_amount = request.POST.get('discount_amount')
        discount_type = request.POST.get('discount_type')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        quantity = request.POST.get('quantity')
        minimum_order_amount = request.POST.get('minimum_order_amount')
        active = request.POST.get('active')

        coupon = Coupons(
            coupon_title=coupon_title,
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            discount_type=discount_type,
            valid_from=valid_from,
            valid_to=valid_to,
            limit=quantity,
            minimum_order_amount=minimum_order_amount,
            active=active,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        coupon.save()

        return redirect('coupons_page')
    return render(request,"admin_panel/add_coupons.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def edit_coupons(request, id):
    coupon = get_object_or_404(Coupons, id=id)

    if request.method == 'POST':
        coupon.coupon_title = request.POST.get('coupon_title')
        coupon.coupon_code = request.POST.get('coupon_code')
        coupon.discount_amount = request.POST.get('discount_amount')
        coupon.discount_type = request.POST.get('discount_type')
        coupon.valid_from = request.POST.get('valid_from')
        coupon.valid_to = request.POST.get('valid_to')
        coupon.limit = request.POST.get('quantity')
        coupon.minimum_order_amount = request.POST.get('minimum_order_amount')
        coupon.active = request.POST.get('active')
        coupon.updated_at = timezone.now()
        coupon.save()
        
        return redirect('coupons_page')

    context = {'coupon': coupon}
    return render(request, 'admin_panel/edit_coupons.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def delete_coupons(request, id):
    coupon = get_object_or_404(Coupons, id=id)

    # Toggle the state of coupon.active
    coupon.active = not coupon.active
    coupon.save()

    return redirect('coupons_page')


def apply_coupon(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        coupon_code = request.POST.get('couponCode', '')
        cart_items = CartItem.objects.filter(user=user).order_by('id')  
        subtotal_price = sum(cart_items.values_list('cart_price', flat=True))

        try:
            coupon = Coupons.objects.get(coupon_code=coupon_code)
        except Coupons.DoesNotExist:
            response_data = {
                'success': False,
                'message': 'Enter a valid coupon code.',
            }
            return JsonResponse(response_data)

        current_date = timezone.now().date()

        if not (coupon.valid_from <= current_date <= coupon.valid_to):
            response_data = {
                'success': False,
                'message': 'Coupon is not valid for the current date.',
            }
            return JsonResponse(response_data)

        if CouponUsage.objects.filter(user=user, coupon=coupon).exists():
            response_data = {
                'success': False,
                'message': 'Coupon has already been used by this user.',
            }
        else:
            if coupon.minimum_order_amount is not None and subtotal_price < coupon.minimum_order_amount:
                response_data = {
                    'success': False,
                    'message': f'Minimum order amount of {coupon.minimum_order_amount} not met for this coupon.',
                }
            else:
                if coupon.limit is not None and CouponUsage.objects.filter(coupon=coupon).count() >= coupon.limit:
                    response_data = {
                        'success': False,
                        'message': 'Coupon limit reached.',
                    }
                else:
                    discount = coupon.discount_amount

                    updated_total_amount = subtotal_price - discount
                    request.session['final_amount'] = int(updated_total_amount)
                    
                    # Create CouponUsage and decrement the coupon limit
                    CouponUsage.objects.create(user=user, coupon=coupon)
                    coupon.limit -= 1
                    coupon.save()

                    response_data = {
                        'success': True,
                        'updated_total_amount': updated_total_amount,
                        'discount_amount': discount,
                    }
                    print(response_data)

    return JsonResponse(response_data)


def remove_coupon(request):
    if request.method == 'POST':
        email = request.session.get('user')
        user = CustomUser.objects.get(email=email)

        total = sum(CartItem.objects.filter(user=user).values_list('cart_price', flat=True))

        response_data = {
                'success': True,
                'updated_total_amount':total,
                'discount_amount': 0,
            }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'})
    
    

    