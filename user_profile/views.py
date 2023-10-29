from django.shortcuts import render,redirect
from user_authentication.models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
# Create your views here.


# function for rendering the user profile page with the user details
def user_profile(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        return render(request, "user_side/user_profile.html", {'user':user})
    else:
        return redirect('signin')
    
    
# function for editing the user profile data 
def update_user_profile(request):
    if request.user.is_authenticated and request.method == 'POST':
        user = request.user
        new_phone_number = request.POST.get('phone_number')
        if CustomUser.objects.exclude(id=user.id).filter(phone_number=new_phone_number).exists():
            messages.error(request, "phone number already exist in the database")
            return redirect('user_profile')
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        return redirect('user_profile')
    else:
        user = CustomUser.objects.get(username=request.user.username)
        return render(request, 'user_side/user_profile.html',{'user':user})
    
# function for reseting the password in the user_profile
def change_password(request):
    if request.user.is_authenticated and request.method == 'POST':
        current_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        new_password_confirm = request.POST.get('new_password')
        
        user = authenticate(username=request.user.username, password=current_password)
        
        if user is not None:
            if new_password == new_password_confirm:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('user_profile')
            else:
                resp = {"error": "New passwords do not match."}
                return JsonResponse(resp, status=400)
        else:
            resp = {"error": "Current password is incorrect."}
            return JsonResponse(resp, status=400)
    else:
        return redirect('signin')