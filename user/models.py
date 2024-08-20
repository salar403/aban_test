from django.db import models
from passlib.hash import argon2

from backend.customs.exceptions import CustomException
from backend.customs.validators import validate_password_strength
from backend.settings import (
    PASSWORD_HASH_LEN,
    PASSWORD_HASH_MAX_MEMORY,
    PASSWORD_HASH_MAX_THREADS,
    PASSWORD_HASH_MAX_TIME,
    PASSWORD_HASH_SALT_LEN,
)


class User(models.Model):
    phone_number = models.CharField(max_length=11, unique=True, null=False)
    email = models.EmailField(max_length=150, unique=True, null=True)
    name = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=500, null=True)
    banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone_number)

    def validate_password(self, password: str):
        if not self.password:
            raise CustomException(code="password_not_set")
        if not argon2.verify(password, self.password):
            raise CustomException(code="wrong_password")

    def set_password(self, password: str):
        validate_password_strength(password)
        self.password = self.hash_password(password=password)
        self.save()

    def hash_password(self, password: str):
        hashed_password = argon2.using(
            max_threads=PASSWORD_HASH_MAX_THREADS,
            hash_len=PASSWORD_HASH_LEN,
            memory_cost=PASSWORD_HASH_MAX_MEMORY,
            salt_len=PASSWORD_HASH_SALT_LEN,
            time_cost=PASSWORD_HASH_MAX_TIME,
        ).hash(password)
        return hashed_password


class Session(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="sessions")
    token_id = models.BigIntegerField(null=False)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=False)
    country = models.CharField(max_length=10, null=True)
    device = models.TextField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} {self.ip} {self.created_at}"
