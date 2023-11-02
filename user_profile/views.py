from django.shortcuts import render, redirect
from user_authentication.models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
from .models import Address
# Create your views here.


#function for rendering user profile with data in it 
def user_profile(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        addresses = Address.objects.filter(user=user)
        return render(request, "user_side/user_profile.html", {'addresses': addresses, 'user':user})
    else:
        return redirect('signin')


# function for editing the user profile data
def update_user_profile(request):
    if 'user' in request.session and request.method == 'POST':
        username = request.session['user']
        user = CustomUser.objects.filter(email=username).first()
        new_phone_number = request.POST.get('phone_number')
        if CustomUser.objects.exclude(id=user.pk).filter(phone_number=new_phone_number).exists():
            messages.error(
                request, "phone number already exist in the database")
            return redirect('user_profile')
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        return redirect('user_profile')
    else:
        # user = CustomUser.objects.get(username=username)
        return render(request, 'user_side/user_profile.html', {'user': user})


# function for reseting the password in the user_profile
def change_password(request):
    if 'user' in request.session and request.method == 'POST':
        current_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        new_password_confirm = request.POST.get('new_password')
        email = request.session['user']

        user = authenticate(username=email,
                            password=current_password)

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

 # function for loading address page


def address_page(request):
    if 'user' in request.session:
        return render(request, 'user_side/address.html')
    else:
        return redirect('signin')


# function for adding new address
def add_address(request):
    if 'user' in request.session and request.method == 'POST':
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pin_code')
        landmark = request.POST.get('land_mark')

        new_address = Address(

            user=user,
            full_name=full_name,
            mobile_number=mobile_number,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            landmark=landmark
        )
        new_address.save()

        return redirect('user_profile')
    else:
        return redirect('signin')


# function for editing user address
def update_address(request, id):
    
    email = request.session['user']
    user = CustomUser.objects.get(email=email)
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pin_code')
        landmark = request.POST.get('land_mark')
        
        address.full_name = full_name
        address.mobile_number = mobile_number
        address.address_line = address_line
        address.city = city
        address.state = state
        address.pincode = pincode
        address.landmark = landmark
        
        address.save()
            
        return redirect('user_profile')
    
    return render(request,'user_side/edit_address.html', {'address':address})


# function for removind address
def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('user_profile')
    