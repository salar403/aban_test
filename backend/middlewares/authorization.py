import binascii
from hashlib import sha512
import hmac, json, base64

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import caches

from user.models import User

from backend.settings import AUTH_TOKEN_PERFIX
from backend.customs.utils import get_object_or_none
from backend.environments import (
    CLIENT_TYPES,
    PAYLOAD_PARAMETERS,
    TOKEN_ID,
    KEY_ID,
    CLIENT_TYPE,
)

user_token_cache = caches["tokens"]
admin_token_cache = caches["admin_tokens"]
key_cache = caches["keys"]


class AuthorizationError(Exception):
    def __init__(self, code: str, status: int) -> None:
        self.code = code
        self.status = status


class CustomAuthorization(MiddlewareMixin):
    def reject(self, code: str = "unauthtenticated", status: int = 401):
        return HttpResponse(
            content=json.dumps({"code": code}),
            status=status,
            content_type="application/json",
        )

    def validate_token(self, token):
        try:
            perfix, token_str = token.split()
            payload, signature = token_str.split(".")
            if perfix != AUTH_TOKEN_PERFIX:
                return
            token_json = json.loads(base64.b64decode(payload).decode())
        except ValueError or binascii.Error or json.JSONDecodeError:
            return
        if (
            not isinstance(token_json, dict)
            or set(token_json).difference(PAYLOAD_PARAMETERS) != set()
            or token_json[CLIENT_TYPE] not in CLIENT_TYPES
        ):
            return
        return (token_json, payload, signature)

    def validate_signature(self, signature: str, key: str, payload: str):
        sign = hmac.new(key.encode(), payload.encode(), sha512).hexdigest()
        return bool(sign == signature)

    def validate_client(
        self, request: object, token_info: dict, payload: str, signature: str
    ):
        user_id = user_token_cache.get(token_info[TOKEN_ID])
        if not user_id:
            return self.reject()
        key = key_cache.get(token_info[KEY_ID])
        if not key:
            return self.reject()
        if self.validate_signature(signature=signature, key=key, payload=payload):
            user = get_object_or_none(User, id=user_id)
            if not user:
                return self.reject()
            request.client = user

    def process_request(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return
        validated_token = self.validate_token(token=token)
        if not validated_token:
            return self.reject()
        token_json, payload, signature = validated_token
        return self.validate_client(request, token_json, payload, signature)
