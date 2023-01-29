from django.shortcuts import render
from .models import Chat, Group
# Create your views here.

def home(request, group_name):
    group, resp = Group.objects.get_or_create(name = group_name)
    chats = []
    if group.has_group:
        chats = group.group_chat.all()
    return render(request,'app/index.html',context={'group_name':group_name,'chats':chats})