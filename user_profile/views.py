from django.shortcuts import render,get_object_or_404
from django.contrib.auth import get_user_model
from .models import Profile
User = get_user_model()

def show_profile(request,username):
    user = get_object_or_404(User,username=username)
    user_profile = get_object_or_404(Profile,user=user)
    return render(request,'user_profile/profile.html',{'profile':user_profile})
