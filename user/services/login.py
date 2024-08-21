from hashlib import sha512
import time, json, random, hmac, base64, secrets

from django.core.cache import caches

from backend.customs.utils import get_object_or_none

from backend.environments import CLIENT_TYPE, KEY_ID, TOKEN_ID, USER_CLIENT_TYPE
from backend.settings import USER_TOKEN_TIMEVALID, TOKEN_KEY_TIMEVALID

from user.models import User

token_key_cache = caches["keys"]
token_cache = caches["tokens"]


class LoginManager:
    def __init__(self) -> None:
        pass

    def generate_new_key(self) -> tuple:
        key_id = random.randint(1, 100000000)
        while token_key_cache.get(key_id) or not token_key_cache.add(
            key_id, secrets.token_urlsafe(32), TOKEN_KEY_TIMEVALID
        ):
            key_id = random.randint(1, 100000000)
        return key_id, token_key_cache.get(key_id)

    def generate_jwt_text(self, token_data: dict, key: str) -> str:
        public_str = base64.b64encode(json.dumps(token_data).encode()).decode()
        signed_str = hmac.new(key.encode(), public_str.encode(), sha512).hexdigest()
        return f"{public_str}.{signed_str}"

    def login_user(
        self,
        user: User,
        timevalid: float = USER_TOKEN_TIMEVALID,
    ) -> dict:
        key_id, token_key = self.generate_new_key()
        token_id = random.randint(1, 100000000)
        while token_cache.get(token_id) or not token_cache.add(
            token_id, user.id, timevalid
        ):
            token_id = random.randint(1, 100000000)
        token_data = {TOKEN_ID: token_id, KEY_ID: key_id, CLIENT_TYPE: USER_CLIENT_TYPE}
        return {
            "token": self.generate_jwt_text(token_data, token_key),
            "timevalid": int(time.time() + timevalid),
            "token_id": token_id,
        }

    def logout_user(self, user: User, token_id: int) -> bool:
        if token_cache.delete(token_id):
            in_db_token = get_object_or_none(
                user.sessions, is_active=True, token_id=token_id
            )
            if in_db_token:
                in_db_token.is_active = False
                in_db_token.save()
            return True
        return False
