from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm
from django.views.generic import View


# def loginPage(request):
#     return HttpResponse("<h1> teryy g </h1>")

   
def loginPage(request):
    page = 'login'
    #form = AuthenticationForm()
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f' Welcome {username}!')
            return redirect('home')
        else:
            messages.info(request, f'Incorrect username or password!')
    return render(request, 'login_register.html', {'title':'log in', 'page':page})

def logoutPage(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        email = request.POST['email'].lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email address taken, try a new one!')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username taken, try a new one!')
            else:
                user= User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully!')
                # login(request, user)
                return redirect('login')
        else:
            messages.error(request, "Password doesn't match!")
    return render(request, 'login_register.html')

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q)| Q(description__icontains=q)) 
    #icontains means checks if the passed parameter is present whether lower or upper case in searches.
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count, 'title':'Study Pad', 'room_messages':room_messages}
    return render(request, 'home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method=='POST':
        message = Message.objects.create(
            user = request.user, room = room, body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'title':'Rooms', 'room_messages':room_messages, 'participants':participants}
    return render(request, 'room.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms,'room_messages':room_messages, 'topics':topics}
    return render(request, 'profile.html', context)

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user, 
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')  
        )
        messages.success(request, f' Room created succesfully!')
        return redirect('home')
        
    context = {'form':form, 'title':'Create Rooms', 'topics':topics}
    return render(request, 'room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not authorized to carry out this operation!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        return redirect('home')
    context = {'form':form, 'title':'Update Rooms', 'topics':topics, 'room':room}
    return render(request, 'room_form.html', context)
    
            
        
@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not authorized to carry out this operation!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj':room, 'title':'Delete Rooms'}
    return render(request, 'delete.html', context)

        
@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not authorized to delete this message!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = {'obj': message, 'title':'Delete Message'}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method=='POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'update_user.html', {'form':form})

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'topics.html', {'topics':topics})

def activity_page(request):
    room_messages = Message.objects.all()
    return render(request, 'activity.html', {'room_messages':room_messages})