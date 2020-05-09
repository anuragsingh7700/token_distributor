from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import views as auth_views
from .models import Event,EventToken
import datetime
from django.db import transaction

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            return render(request,'signup.html',{'form':form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
        else:
            form = login()
            return render(request, 'login.html', {'title':"Sign Up",'form': form})
    else:
        return render(request,auth_views.LoginView.as_view(template_name ='login.html'))

@login_required(login_url='/home/login/')
def home(request):
    return render(request, 'index.html')

@login_required(login_url='/home/login/')
def event_list(request):
    events = Event.objects.all()
    return render(request,"eventlist.html",{'Event':events})

@login_required(login_url='/home/login/')
def gen_token(request,id):
    #database queries
    allotted_tokens = EventToken.objects.filter(event_id = id).order_by('-token_id','id')
    event = Event.objects.filter(id=id)[0]
    #if first token
    if not allotted_tokens:
        try:
            new_token = EventToken(event_id = event,token_id = 1,timing=datetime.time(event.time.hour, event.time.minute,0) ,username=request.user.username)
            new_token.save()
            return render(request,"token.html",{'message':"Token Generated",'token':new_token})
        except:
            transaction.rollback()
            return render('/home/events/',{"message":"Token Generation Failed!\nPlease Try again!"})

    #checking user for already taken token
    for token in allotted_tokens:
        if request.user.username == token.username:
            return render(request,"token.html",{'message':"Token already taken",'token':token})

    #id related operations
    last_token = allotted_tokens[0]
    last_token_id = last_token.token_id

    #timing related operations
    last_timing = last_token.timing
    event_timeslot = datetime.time(hour=0,minute=event.timeslot_in_mins,second=0)
    new_hour_time = last_timing.hour
    new_mins_time = event_timeslot.minute + last_timing.minute 
    if new_mins_time / 60 > 1:
        new_hour_time += 1
        new_mins_time -= 60
    new_timing = datetime.time(new_hour_time,new_mins_time,0)

    try :
        new_token = EventToken(event_id = event,token_id = last_token_id + 1,timing=new_timing,username=request.user.username)
        new_token.save()
        return render(request,"token.html",{'message':"Token Generated",'token':new_token})
    except:
        transaction.rollback()
        all_events = Event.objects.all()
        msg = "Token Generation Failed!\nPlease Try again!"
        return render(request,'eventlist.html',{"Event":all_events,"msg":msg})


@login_required(login_url='/home/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/home/login/')
def token_list(request):
    allotted_tokens = EventToken.objects.filter(username = request.user.username)
    events = Event.objects.values('id','name','time')
    print(events)
    print(allotted_tokens)
    return render(request,'tokenlist.html',{'tokens':allotted_tokens,'event':events})