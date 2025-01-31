from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from home.views import index
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def register(request):
    template_data = {}
    template_data = {'title': 'Register'}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Log the user in after registration
            # usually doesn't it not login after registration, just boot you back to login?
            return redirect("login")  # Redirect to landing page
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form, "template_data": template_data})

def user_login(request):
    template_data = {}
    template_data = {'title': 'Login'}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect(successful_login)  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form, "template_data": template_data})

def user_logout(request):
    logout(request)  # Logs the user out
    return redirect(index)  # Redirect to the landing page (or any other page)

@login_required
def profile(request):
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})

def password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            # Generate a token and UID for the user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            return redirect("password_reset_confirm", uidb64=uid, token=token)
        except User.DoesNotExist:
            return render(request, "accounts/password_reset.html", {"error": "User not found"})
    return render(request, "accounts/password_reset.html")

def password_reset_confirm(request):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("password_reset_complete")
    else:
        form = SetPasswordForm(request.user)
    return render(request, "accounts/password_reset_confirm.html", {"form": form})

def successful_login(request):
    template_data = {}
    template_data = {'title': 'Success'}
    return render(request, 'accounts/temp_success.html', {"template_data": template_data})