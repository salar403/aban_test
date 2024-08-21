from unidecode import unidecode
from rest_framework import serializers

from user.models import Session, User


from user.services.login import LoginManager

from backend.customs.exceptions import CustomException
from backend.customs.utils import get_object_or_none
from backend.customs.validators import validate_phone_number


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True, allow_null=True, allow_blank=False
    )
    password = serializers.CharField(required=True, allow_null=False, allow_blank=True)

    def validate_phone_number(self, phone_number):
        phone_number = unidecode(phone_number)
        validate_phone_number(phone_number=phone_number)
        self._user = get_object_or_none(User, phone_number=phone_number)
        if not self._user:
            raise CustomException(code="login_unknown")
        return phone_number

    def validate_password(self, password: str):
        self._user.validate_password(password=password)
        return password

    def create(self, validated_data):
        request = self.context.get("request")
        token_data = LoginManager().login_user(user=self._user)
        Session.objects.create(
            user=self._user,
            ip=request.ip,
            device=request.device,
            country=request.country,
            token_id=token_data["token_id"],
        )
        token_data["code"] = "login_success"
        token_data.pop("token_id")
        self._data = token_data
        return token_data


class LogoutSerializer(serializers.Serializer):
    def validate(self, validated_data):
        user = self.context["request"].client
        if not user:
            raise CustomException(code="unauthtenticated", status_code=401)
        return validated_data

    def create(self, validated_data):
        request = self.context["request"]
        LoginManager().logout_user(user=request.client, token_id=request.token_id)
        self._data = {"code": "logout_success"}
        return True
