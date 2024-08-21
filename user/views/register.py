from rest_framework import status

from backend.customs.views import CreateApiView
from user.serializers.register import UserRegisterSerializer


class RegisterByMobile(CreateApiView):
    serializer_class = UserRegisterSerializer
    context_map = {"request": None}
    response_code = status.HTTP_201_CREATED
