from rest_framework import status

from backend.customs.views import CreateApiView, DestroyApiView

from backend.customs.permissions import IsAuthenticated
from user.serializers.auth import LoginSerializer, LogoutSerializer


class Login(CreateApiView):
    serializer_class = LoginSerializer
    context_map = {"request": None}
    response_code = status.HTTP_200_OK


class Logout(DestroyApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    context_map = {"request": None}
    response_code = status.HTTP_200_OK
