from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from user_authentication.models import CustomUser
from .models import Thread,ChatMessage


def chatpage(request):
    if 'user' in request.session:
        email = request.session['user']
        user =  CustomUser.objects.get(email=email)
        
    context = {
        'user': user   
    }
    return render(request, 'chatss/chatpage.html',context)

def admin_chatpage(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    print(request.user)
    context = {
        'Threads': threads,    
    }
    return render(request, 'admin_panel/admin_chat.html',context)


