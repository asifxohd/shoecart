from django.shortcuts import render
from orders.models import OrdersItem, Orders
from django.db.models import Sum, Count, Q ,Value, F
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from admin_home.models import Category,Product
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db import models
from decimal import Decimal



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_dash(request):
    # Get all categories
    categories = Category.objects.all()

    # Count of orders with payment status 'success' for each category
    order_count_by_category = (
        categories.annotate(
            order_count=Count(
                'product__sizevariant__ordersitem__order',
                filter=Q(product__sizevariant__ordersitem__payment_status='success')
            )
        )
    )

    # Count of all orders excluding temporary and refunded orders
    no_of_orders = Orders.objects.filter(ordersitem__payment_status='success').distinct().count()

    # Calculate total revenue
    total_revenue = OrdersItem.objects.filter(payment_status='success').aggregate(
        total_revenue=Sum(F('quantity') * F('price'), output_field=models.DecimalField(max_digits=10, decimal_places=2))
    )
    print(total_revenue)
    total_revenue_value = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0
    total_profit = round(total_revenue_value * Decimal('0.3'), 2)

    # Count total number of customers (excluding temporary orders)
    total_customers = Orders.objects.exclude(ordersitem__payment_status="temp").values('user').distinct().count()

    # Count orders with payment method 'COD', 'onlinePayment', and 'wallet'
    total_cash_on_delivery = Orders.objects.filter(payment_method='COD').count()
    total_online = Orders.objects.filter(payment_method='onlinePayment').exclude(ordersitem__payment_status="temp").count()
    total_wallet = Orders.objects.filter(payment_method='wallet').count()

    # Gather order data for plotting
    order_data = Orders.objects.filter(ordersitem__payment_status='success').values('order_date').annotate(order_count=Count('pk'))
    customer_data = Orders.objects.exclude(ordersitem__payment_status="temp").values('order_date', 'user').distinct().annotate(customer_count=Count('user'))

    order_counts = [entry['order_count'] for entry in order_data]
    customer_counts = [entry['customer_count'] for entry in customer_data]
    nested_order_data = [[category.name, category.order_count] for category in order_count_by_category]

    # Get the most sold products
    most_sold_products = (
        Product.objects
        .annotate(total_quantity_sold=Coalesce(Sum('sizevariant__ordersitem__quantity'), Value(0)))
        .order_by('-total_quantity_sold')[:4]
        .values_list('name', 'total_quantity_sold')
    )

    # Prepare the context for rendering
    context = {
        'no_of_orders': no_of_orders,
        'total_revenue': int(total_revenue_value),
        'total_customers': total_customers,
        'total_cash_on_delivery': total_cash_on_delivery,
        'total_online': total_online,
        'total_wallet': total_wallet,
        'cat': categories,
        'nested_order_data': nested_order_data,
        'order_counts': order_counts,
        'customer_counts': customer_counts,
        'most_sold': most_sold_products,
        'profit': total_profit
    }

    # Render the admin dashboard template with the provided context
    return render(request, "admin_panel/admin_dash.html", context)



# Function for rendering the admin side sales report page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_sales(request):
    # Retrieve delivered orders with payment status 'success' and order by order date
    delivered_orders = Orders.objects.filter(ordersitem__payment_status='success').order_by('-order_date').distinct()    
    context = {
        'recent_orders': delivered_orders
    }
    return render(request, 'admin_panel/sales_report.html', context)


# Function for sales report page by the date filter
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def filter_by_date_sales_report(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve 'from_date' and 'to_date' from the POST data
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        print(from_date)
        print(to_date)

        # Filter delivered orders based on the date range if 'from_date' and 'to_date' are provided
        if from_date and to_date:
            delivered_orders = Orders.objects.filter(ordersitem__payment_status='success', order_date__range=[from_date, to_date]).order_by('-order_date').distinct()  
        else:
            delivered_orders = 0
        
        context = {
            'recent_orders': delivered_orders
        }
    return render(request, 'admin_panel/sales_report.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def datefilter_dashboard(request):
    # Retrieve the type of date filter (day, week, year) from the POST request
    date_type = request.POST.get('button')
    
    # Get the current date
    current_date = datetime.now().date()
    
    # Initialize the start_date variable
    start_date = None

    # Determine the start date based on the selected date type
    if date_type == 'day':
        start_date = current_date
    elif date_type == 'week':
        start_date = current_date - timedelta(days=current_date.weekday())
    elif date_type == 'year':
        start_date = datetime(current_date.year, 1, 1).date()

    # Calculate the total revenue for successful orders within the specified date range
    total_revenue = OrdersItem.objects.filter(payment_status='success', order__order_date__gte=start_date).aggregate(
        total_revenue=Sum(F('quantity') * F('price'), output_field=models.DecimalField(max_digits=10, decimal_places=2))
    )

    # Calculate the number of successful orders within the specified date range
    no_of_orders = Orders.objects.filter(ordersitem__payment_status='success', order_date__gte=start_date).distinct().count()

    # Extract the total revenue value or set it to 0 if None
    total_revenue_value = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0
    
    # Calculate the total profit (30% of total revenue)
    total_profit = round(total_revenue_value * Decimal('0.3'), 2)

    # Create a dictionary with the calculated values
    data = {
        'total_revenue': int(total_revenue_value),
        'no_of_orders': no_of_orders,
        'total_profit': total_profit,
    }

    # Delete temporary orders with payment_status="temp"
    Orders.objects.filter(ordersitem__payment_status="temp").delete()
    
    # Return the calculated data as a JSON response
    return JsonResponse(data)


