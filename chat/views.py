from django.shortcuts import render, redirect
from user_authentication.models import CustomUser
from .models import Thread,ChatMessage
from django.shortcuts import render, get_object_or_404


def chatpage(request):
    # Check if 'user' is in the session
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        admin = CustomUser.objects.get(username='admin')
        # Check if a thread exists between the user and admin
        thread = Thread.objects.filter(first_person=user, admin=admin).first()
        old_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp') if thread else None
        context = {
            'user': user,
            'old_messages': old_messages,
        }
        return render(request, 'chatss/chatpage.html', context)
    else:
        # Redirect to signin if 'user' is not in the session
        return redirect('signin')

def admin_chatpage(request):
    # Retrieve threads associated with the current user (admin)
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    context = {
        'Threads': threads,
    }
    return render(request, 'admin_panel/admin_chat.html', context)

def admin_chat(request, thread_id, recipient_id):
    # Retrieve the thread and recipient user based on thread_id and recipient_id
    thread = get_object_or_404(Thread, id=thread_id, admin=request.user)
    recipient_user = get_object_or_404(CustomUser, username=recipient_id)
    # Retrieve old messages for the thread
    old_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
    context = {
        'Thread': thread,
        'RecipientUser': recipient_user,
        'old_messages': old_messages,
    }
    return render(request, 'admin_panel/admin_chat_messages.html', context)

