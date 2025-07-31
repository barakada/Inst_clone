from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                login=form.cleaned_data.get('identifier'),
                password=form.cleaned_data.get('password'),
            )
            if user is not None:
                login(request, user)
                return redirect('user_profile:show_profile')
            else:
                form.add_error(None,"Invalid login or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('accounts:login')
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form})
