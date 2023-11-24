from django.urls import path
from . import views

urlpatterns = [ 
    path('chatpage', views.chatpage, name='chatpage'),
    path('admin_chatpage', views.admin_chatpage, name='admin_chatpage'),
    path('admin_chat/<int:thread_id>/<str:recipient_id>/', views.admin_chat, name='admin_chat'),

]
