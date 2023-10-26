from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.core.mail import send_mail
import random
from datetime import datetime, timedelta
from .models import CustomUser  

# Function to send a 6-digit OTP email to the user
def send_6_digit_otp_email(request):
    if request.user.is_authenticated:
        return redirect('homepage')  
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
    if request.user.is_authenticated:
        return redirect('homepage')    
    
    if request.method == 'POST':
        first_name = request.POST['firstname']
        phone_number = request.POST['phonenumber']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        request.session['recipient_email'] = email

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.info(request, 'Phone number is taken')
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
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        email = request.POST['email']
        
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active == False:
                messages.error("user Access denied")
                return redirect('signin')
            if user.email_verified:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, 'Email is not verified.')
                return redirect('signin')
        else:
            messages.error(request, 'Invalid password. Please try again.')
            return redirect('signin')

    return render(request, 'user_auth/loginpage.html')


# function for otp page
def otp(request):
    if request.user.is_authenticated:
        return redirect('homepage') 
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            user_data = request.session.get('registration_data')
            if user_data:
                user = CustomUser.objects.create_user(
                    username = user_data['email'],
                    first_name=user_data['firstname'],
                    last_name=user_data['lastname'],
                    email=user_data['email'],
                    password=user_data['password'],
                    phone_number=user_data['phonenumber'],
                    email_verified = True
                )
                user.save()
                
                del request.session['registration_data']
                return redirect('signin')
                
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'user_auth/otppage.html')


# function for userlogout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')
