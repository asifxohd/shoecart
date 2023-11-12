from django.shortcuts import render
from .models import Wallet
from user_authentication.models import CustomUser
import razorpay
from django.http import JsonResponse
import secrets
from django.utils import timezone  # Import timezone module



client = razorpay.Client(auth=('rzp_test_F83XKwHAQwFDZG', 'etDY4jG2xDLoFngOnDsM7wqY'))
# function for rendering wallet page on the user profile
def wallet_page(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        wallet_details = Wallet.objects.filter(user=user).order_by('-id')
        if wallet_details:
            balance = wallet_details.first().balance
        else:
            balance = 0
            
        return render(request, 'user_side/wallet.html',{'wallet_details':wallet_details, 'user':user , 'balance':balance})
        
    return render(request, 'user_side/wallet.html')
    
    
def collect_payment_details(request):
    try:
        print("money coming")

        # Get amount from the request body
        amount = int(request.POST.get('amountToAdd'))
        print('amount', amount)
        request.session['walletmoney'] = amount
        
        # Generate a random receipt ID
        receipt_id = secrets.token_hex(4)

        # Set up options for creating a Razorpay order
        options = {
            'amount': amount * 100,  
            'currency': 'INR',
            'receipt': receipt_id,
        }

        # Create a Razorpay order
        razorpay_order = client.order.create(options)
        print(razorpay_order)

        # Return the response
        return JsonResponse({'status': True, 'payment': razorpay_order})

    except Exception as e:
        print(e)
        return JsonResponse({'status': False})
    
    
def verify_wallet_payment(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        amount = request.session['walletmoney']

        last_transaction = Wallet.objects.filter(user=user).last()

        if last_transaction:
            new_balance = last_transaction.balance + amount
        else:
            new_balance = amount

        payment = Wallet(
            user=user,
            transaction_details=f'Rs. {amount}.00 Deposit to the wallet',
            transaction_type="Credit",
            transaction_amount=amount,
            balance=new_balance,
            date=timezone.now()
        )
        payment.save()

        return JsonResponse({'success': True})

    else:
        return JsonResponse({'success': False})
