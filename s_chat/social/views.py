
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile, Tweep
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, TweeForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from rest_framework.authtoken.models import Token




# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = TweeForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweep = form.save(commit=False)
                tweep.user = request.user
                tweep.save()
                messages.success(request, ('Your Tweep hasbeen Posted'))
                return redirect('home') 
        tweeps = Tweep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweeps": tweeps, "form": form})
    else:
        tweeps = {messages: "no tweeps"}
        return render(request, 'home.html',)
    
# Liking a Tweep
    
def Likes(request):
    if request.method == 'POST':
        tweep_id = request.POST.get('tweep_id')
        if tweep_id:
            tweep = Tweep.objects.get(id=tweep_id)
            # Increment the like count
            tweep.likes.add(request.user)
            tweep.save()
    tweeps = Tweep.objects.all()
    return render(request, 'home.html', {'tweeps': tweeps})

def profile_list(request, massege=None):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'You Must First Log in to continue..!')

        return HttpResponseRedirect('/')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        user_tweeps = Tweep.objects.filter(user_id=pk)
        tokens = Token.objects.filter(user_id=pk)
        
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # get Form Data
            action  = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
        
        # Save the profiles
        
            current_user_profile.save()
        
            
        return  render(request, 'profile.html', {"profile": profile, "user_tweeps": user_tweeps,'tokens': tokens})
    else:
        messages.success(request, 'You Must First Log in to continue..!')

        return HttpResponseRedirect('/')



def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = authenticate(username=username,email=email, password=password, first_name=first_name,last_name=last_name)
            #Generate tokens for the newly registered user
        
           

            login(request, user)  # Log the user in after registration
            messages.success(request, ("You have successfully Registered!! Welcome...!"))
            return redirect('home')  # Replace 'home' with the name of your home view
    
        
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username= username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Loged in"))
            
            return redirect('home')  # Replace 'home' with the name of your home view
        else:
            messages.success(request,"Log in failed")
            return redirect('login')
    else:
        
        return render(request, 'login.html', {})




def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your home view



# APIs Views
