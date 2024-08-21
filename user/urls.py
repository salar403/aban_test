from django.urls import path
from user.views import auth, register

urlpatterns = [
    #generics
    path("register/mobile/", register.RegisterByMobile.as_view(), name="user_register_mobile"),
    path("login/", auth.Login.as_view(), name="user_login"),
    path("logout/", auth.Logout.as_view(), name="user_logout"),
]
