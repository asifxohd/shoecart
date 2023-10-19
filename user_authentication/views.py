from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser  # Import your user model



# @require_POST
# @csrf_exempt  # This decorator may be necessary to bypass CSRF protection for AJAX requests
# def check_email_exists(request):
#     email = request.POST.get('email')
#     exists = CustomUser.objects.filter(email=email).exists()
#     return JsonResponse({'exists': exists})

# @require_POST
# @csrf_exempt  # This decorator may be necessary to bypass CSRF protection for AJAX requests
# def check_phone_exists(request):
#     phone_number = request.POST.get('phoneNumber')
#     exists = CustomUser.objects.filter(phone_number=phone_number).exists()
#     return JsonResponse({'exists': exists})



# Function to send a 6-digit OTP email to the user
def send_6_digit_otp_email(request):
    # Generate a random 6-digit OTP
    otp = random.randint(100000, 999999)
    request.session['otp'] = str(otp)

    # Calculate the OTP expiration time (36 seconds from now)
    expiration_time = datetime.now() + timedelta(seconds=36)
    request.session['otp_expiration_time'] = expiration_time.strftime("%Y-%m-%d %H:%M:%S")

    # Calculate remaining time in seconds
    remaining_time_seconds = max(0, (expiration_time - datetime.now()).total_seconds())

    # Send the OTP in the email
    subject = 'Your 6-digit OTP for email verification'
    message = f'Your ShoeCart Email Verification OTP: {otp}\n\nPlease keep this code confidential.\n\nThank you for choosing ShoeCart.\n\nSincerely, The ShoeCart Team'
    from_email = 'asifxohd@gmail.com'
    recipient_email = request.session.get('recipient_email')
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return render(request, 'user_auth/otppage.html', {'remaining_time_seconds': remaining_time_seconds, 'expiration_time': expiration_time.timestamp(), 'current_time': datetime.now().timestamp()})


# Handle user registration
def signup(request):   
    if request.method == 'POST':
        # Extract user information from the form
        first_name = request.POST['firstname']
        phone_number = request.POST['phonenumber']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        request.session['recipient_email'] = email

        # Check if the phone number or email is already registered
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is taken')
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken')
            return redirect('signup')
        else:
            request.session['registration_data'] = {
            'firstname': first_name,
            'phonenumber': phone_number,
            'lastname': last_name,
            'email': email,
            'password': password,
            }
            return redirect('send_otp')


    return render(request, 'user_auth/signup.html')

# Handle user login
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.email_verified:
                print(user.email_verified)
                return redirect('homepage')
            else:
                messages.error(request, 'Email is not verified.')
                return redirect('signin')
        else:
            messages.error(request, 'Invalid password. Please try again.')
            return redirect('signin')

    return render(request, 'user_auth/loginpage.html')

def otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            # User creation after successful OTP verification
            user_data = request.session.get('registration_data')
            if user_data:
                user = CustomUser.objects.create_user(
                    username = user_data['email'],
                    first_name=user_data['firstname'],
                    last_name=user_data['lastname'],
                    email=user_data['email'],
                    password=user_data['password'],
                    phone_number=user_data['phonenumber'],
                )
                user.save()
                messages.success(request, 'User created successfully')
                del request.session['registration_data']
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid registration data')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'user_auth/otppage.html')

