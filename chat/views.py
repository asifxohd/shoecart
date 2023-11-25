from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_authentication.models import CustomUser
from .models import Thread,ChatMessage
from django.shortcuts import render, get_object_or_404


def chatpage(request):
    
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        admin = CustomUser.objects.get(username='admin')
        print(admin)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        thread = Thread.objects.filter(first_person=user, admin=admin).first()
        print(thread)
        if thread:
            old_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
        else:
            old_messages = None

        context = {
            'user': user,
            'old_messages': old_messages,
        }
        return render(request, 'chatss/chatpage.html', context)
    else:
        return redirect('signin')



def admin_chatpage(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    context = {
        'Threads': threads,    
    }
    return render(request, 'admin_panel/admin_chat.html', context)


def admin_chat(request, thread_id, recipient_id):
    thread = get_object_or_404(Thread, id=thread_id, admin=request.user)
    recipient_user = get_object_or_404(CustomUser, username=recipient_id)
    old_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
    print(old_messages)
    
    context = {
        'Thread': thread,
        'RecipientUser': recipient_user,
        'old_messages': old_messages,
        
    }

    return render(request, 'admin_panel/admin_chat_messages.html', context)


