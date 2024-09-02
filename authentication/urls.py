from .views import UserRegistration,UserLogin
from django.urls import path

urlpatterns=[
    path("register/" ,UserRegistration.as_view(),name="UserRegister"),
    path("login/" ,UserLogin.as_view(),name="UserLogin")
            ]