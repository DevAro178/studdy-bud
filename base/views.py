from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm

# Create your views here.

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'User not found')
            
        user =authenticate(request,email=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email or password doesnot exist')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def RegisterPage(request):
    page='register'
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error occured while registration...')
            
    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)
    
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topic=Topic.objects.all().order_by('-id')[:5]
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'data':rooms,'topic':topic,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participant=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'data':room,'room_messages':room_messages,'participants':participant}
    return render(request,'base/room.html',context)

def user_profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topic=Topic.objects.all()
    context={'user':user,'data':rooms,'room_messages':room_messages,'topic':topic}
    return render(request,'base/profile.html',context)


@login_required(login_url='/login')
def createroom(request):
    form=RoomForm()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    
    topics=Topic.objects.all()
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not permitted to take action here.')
    
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    topics=Topic.objects.all()
    context={'form':form,'topics':topics,'room':room}
    return render(request,"base/room_form.html",context)

@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not permitted to take action here.')
    if request.method=='POST':
        room.delete()        
        return redirect('home')
    context={'obj':room}
    return render(request,'base/delete.html',context)


@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not permitted to take action here.')
    if request.method=='POST':
        message.delete()        
        return redirect('home')
    context={'obj':message}
    return render(request,'base/delete.html',context)

    
@login_required(login_url='/login')
def userSetting(request):
    user=request.user
    imgUrl=request.user.avatar.url
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST , request.FILES, instance=user)
        if form.is_valid:
            form.save() 
            return redirect('user-profile',pk=user.id)
    context={'form':form,'imgUrl':imgUrl}
    return render(request,'base/settings.html',context)


def browseTopics(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    # rooms=Room.objects.filter(
    #     Q(topic__name__icontains=q) |
    #     Q(name__icontains=q) |
    #     Q(description__icontains=q)
    #     )
    topic=Topic.objects.filter(
        Q(name__icontains=q)
    )
    context={'topic':topic}
    return render(request,'base/topics.html',context)

def activityFeed(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)