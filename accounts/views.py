from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

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

def successful_login(request):
    template_data = {}
    template_data = {'title': 'Success'}
    return render(request, 'accounts/temp_success.html', {"template_data": template_data})