from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import HttpResponse

# authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# forms and models
from login_app.models import Profile
from login_app.forms import ProfileForm, SignupForm

#  for show messages
from django.contrib import messages


# Create your views here.
def cbbb(request):
    return render(request, 'base.html')


def sign_up(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully ")
            return HttpResponseRedirect(reverse('Login_App:login'))
    return render(request, 'login_app/signup.html', context={'form': form})


# login view
def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Shop_App:home'))
    return render(request, 'login_app/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out")
    return HttpResponseRedirect(reverse('Shop_App:home'))


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "change Saved")
        form = ProfileForm(instance=profile)
    return render(request, 'login_app/changeprofile.html', context={'form': form})
