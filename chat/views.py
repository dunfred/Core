from chat.models import ChatGroup, Profile
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from django.db.models import  Count, Value, Case, When, CharField
from django.db.models.functions import  Concat, Cast

# Create your views here.
@login_required(login_url='../../admin/login/')
def index(request):
    all_groups = ChatGroup.objects.all()
    context = {
        'groups': all_groups
    }

    return render(request, 'index.html', context)

@login_required(login_url='../../admin/login/')
def room(request, room_name):
    group = ChatGroup.objects.get(id=int(room_name))
    group_name = group.name
    context = {
        'room_name':room_name,
        'group_name': group_name
    }
    if request.user.is_authenticated and not request.user.groups.filter(id=group.id).exists():
        group.user_set.add(request.user)

    return render(request, 'chat.html', context)    

    