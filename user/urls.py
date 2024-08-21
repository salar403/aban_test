from django.urls import path
from user.views import auth, register

urlpatterns = [
    #generics
    path("register/mobile/send/", register.RegisterSendOtp.as_view(), name="user_register_send"),
    path("register/mobile/verify/", register.RegisterVerifyOtp.as_view(), name="user_register_verify"),
    path("login/", auth.Login.as_view(), name="user_login"),
    path("logout/", auth.Logout.as_view(), name="user_logout"),
]
