from django.test import RequestFactory
from django.urls import reverse

from backend.customs.testclasses import UserTestCase, RequestFactory

from user.views import auth


class UserAuthViewsTest(UserTestCase):
    def setUp(self):
        super().setUp()

    def test_phone_login_user(self):
        data = {
            "phone_number": "09000000000",
            "password": "Salamsalam@123",
        }
        request = RequestFactory().post(reverse("user_login"), data=data)
        response = auth.Login.as_view()(request)
        assert response.status_code == 200 and response.data["code"] == "login_success"

    def test_invalid_login_input(self):
        data = {
            "phone_number": "09123456789",
            "password": "test_password",
        }
        request = RequestFactory().post(reverse("user_login"), data=data)
        response = auth.Login.as_view()(request)
        assert (
            response.status_code == 400
            and response.data["code"] == "login_unknown"
            and list(response.data) == ["code"]
        )

    def test_login_wrong_password(self):
        data = {
            "phone_number": "09000000000",
            "password": "test_password",
        }
        request = RequestFactory().post(reverse("user_login"), data=data)
        response = auth.Login.as_view()(request)
        assert (
            response.status_code == 400
            and response.data["code"] == "wrong_password"
            and list(response.data) == ["code"]
        )

    def test_login_wrong_phone_number(self):
        data = {
            "phone_number": "090000000010",
            "password": "test_password",
        }
        request = RequestFactory().post(reverse("user_login"), data=data)
        response = auth.Login.as_view()(request)
        assert (
            response.status_code == 400
            and response.data["code"] == "invalid_phone"
            and list(response.data) == ["code"]
        )
