from django.shortcuts import render
from orders.models import OrdersItem, Orders
from django.db.models import Sum, Count, Q  
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from admin_home.models import Category, SizeVariant


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_dash(request):
    # Get all categories
    categories = Category.objects.all()

    # Count of orders with payment status 'success' for each category
    order_count_by_category = (
        categories
        .annotate(order_count=Count('product__sizevariant__ordersitem__order', filter=Q(product__sizevariant__ordersitem__order__payment_status='success')))
    )

    # Additional metrics (similar to your existing code)
    no_of_orders = Orders.objects.exclude(payment_status="temp").count()
    total_revenue = OrdersItem.objects.filter(order__payment_status='success').aggregate(total_revenue=Sum('price'))
    total_customers = Orders.objects.exclude(payment_status="temp").values('user').distinct().count()
    total_cash_on_delivery = Orders.objects.filter(payment_method='COD').count()
    total_online = Orders.objects.filter(payment_method='onlinePayment').exclude(payment_status="temp").count()
    total_wallet = Orders.objects.filter(payment_method='wallet').count()

    order_data = Orders.objects.filter(payment_status='success').values('order_date').annotate(order_count=Count('pk'))
    revenue_data = OrdersItem.objects.filter(order__payment_status='success').values('order__order_date').annotate(total_revenue=Sum('price'))
    customer_data = Orders.objects.exclude(payment_status="temp").values('order_date', 'user').distinct().annotate(customer_count=Count('user'))

    # Extract data for chart
    dates = [entry['order_date'] for entry in order_data]
    order_counts = [entry['order_count'] for entry in order_data]
    revenue_counts = [entry['total_revenue'] for entry in revenue_data]
    customer_counts = [entry['customer_count'] for entry in customer_data]

    # Create a nested list with category name and order count
    nested_order_data = [[category.name, category.order_count] for category in order_count_by_category]
    print(nested_order_data)

    context = {
        'no_of_orders': no_of_orders,
        'total_revenue': int(total_revenue['total_revenue']) if total_revenue['total_revenue'] else 0,
        'total_customers': total_customers,
        'total_cash_on_delivery': total_cash_on_delivery,
        'total_online': total_online,
        'total_wallet': total_wallet,
        'cat': categories,  # Pass categories to the template
        'nested_order_data': nested_order_data,  # New data structure
        'order_counts': order_counts,  # Include order counts in context
        'revenue_counts': revenue_counts,  # Include revenue counts in context
        'customer_counts': customer_counts,  # Include customer counts in context
        'dates': dates,  # Include dates in context
    }

    return render(request, "admin_panel/admin_dash.html", context)


# function for rendering the admin side sales report page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_sales(request):
    delivered_orders = Orders.objects.filter(payment_status='success').order_by('-order_date').distinct()    
    context = {
        'recent_orders': delivered_orders
    }
    return render(request, 'admin_panel/sales_report.html', context)


# function for sales report page by the date fileter
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def filter_by_date_sales_report(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        print(from_date)
        print(to_date)
        if from_date and to_date:
            delivered_orders = Orders.objects.filter(payment_status='success',order_date__range=[from_date, to_date]).order_by('-order_date').distinct()  
        else:
            delivered_orders = 0
        
        context = {
        'recent_orders': delivered_orders
    }
    return render(request, 'admin_panel/sales_report.html', context)