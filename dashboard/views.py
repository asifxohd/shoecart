from django.shortcuts import render
from orders.models import OrdersItem, Orders
from django.db.models import Sum, Count
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from admin_home.models import Category, SizeVariant



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_dash(request):
    # Count of orders with payment status 'success' for each category
    order_count_by_category = (
        SizeVariant.objects.filter(ordersitem__order__payment_status='success')
        .values('product__category__name')
        .annotate(order_count=Sum('ordersitem__quantity'))
    )
    print(order_count_by_category)
    # Additional metrics (similar to your existing code)
    no_of_orders = Orders.objects.exclude(payment_status="temp").count()
    total_revenue = OrdersItem.objects.filter(order__payment_status='success').aggregate(total_revenue=Sum('price'))
    total_customers = Orders.objects.exclude(payment_status="temp").values('user').distinct().count()
    total_cash_on_delivery = Orders.objects.filter(payment_method='COD').count()
    total_online = Orders.objects.filter(payment_method='onlinePayment').exclude(payment_status="temp").count()
    total_wallet = Orders.objects.filter(payment_method='wallet').count()
    cat = Category.objects.all()
    
    order_data = Orders.objects.filter(payment_status='success').values('order_date').annotate(order_count=Count('pk'))
    revenue_data = OrdersItem.objects.filter(order__payment_status='success').values('order__order_date').annotate(total_revenue=Sum('price'))
    customer_data = Orders.objects.exclude(payment_status="temp").values('order_date', 'user').distinct().annotate(customer_count=Count('user'))


    # Extract data for chart
    dates = [entry['order_date'] for entry in order_data]
    order_counts = [entry['order_count'] for entry in order_data]
    revenue_counts = [entry['total_revenue'] for entry in revenue_data]
    customer_counts = [entry['customer_count'] for entry in customer_data]

    # Create a nested list with category name and order count
    nested_order_data = [ [x['product__category__name'], x['order_count']] for x in order_count_by_category ]
    
    context = {
        'no_of_orders': no_of_orders,
        'total_revenue': int(total_revenue['total_revenue']) if total_revenue['total_revenue'] else 0,
        'total_customers': total_customers,
        'total_cash_on_delivery': total_cash_on_delivery,
        'total_online': total_online,
        'total_wallet': total_wallet,
        'cat': cat,
        'nested_order_data': nested_order_data,  # New data structure
        'order_counts': order_counts,  # Include order counts in context
        'revenue_counts': revenue_counts,  # Include revenue counts in context
        'customer_counts': customer_counts,  # Include customer counts in context
        'dates': dates,  # Include dates in context
    }

    return render(request, "admin_panel/admin_dash.html", context)