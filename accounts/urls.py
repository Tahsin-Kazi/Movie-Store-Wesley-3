from django.urls import path
from accounts.views import register, user_login, successful_login

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("success/", successful_login, name="success"),
]