import re
from backend.customs.exceptions import CustomException


def validate_phone_number(phone_number: str) -> None:
    if (
        type(phone_number) != str
        or len(phone_number) != 11
        or not phone_number.isnumeric()
        or phone_number[0:2] != "09"
    ):
        raise CustomException(code="invalid_phone", status_code=400)


def validate_password_strength(password: str) -> bool:
    if not re.match(
        "(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&/*-_]).{8,}$", password
    ):
        raise CustomException(code="weak_password", status_code=400)
