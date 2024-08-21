from unidecode import unidecode
from rest_framework import serializers
from django.db import IntegrityError, transaction

from backend.customs.exceptions import CustomException
from user.models import User

from backend.customs.validators import validate_phone_number


class UserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, phone_number):
        phone_number = unidecode(phone_number)
        validate_phone_number(phone_number=phone_number)
        return phone_number

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create(
                    phone_number=validated_data["phone_number"],
                    name=validated_data["name"],
                )
                user.set_password(password=validated_data["password"])
        except IntegrityError:
            raise CustomException(code="already_exists")
        self._data = {"code": "register_success"}
        return True
