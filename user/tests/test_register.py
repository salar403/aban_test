from django.test import RequestFactory
from django.urls import reverse

from backend.customs.testclasses import UserTestCase, RequestFactory

from user.views import register


class UserRegisterViewsTest(UserTestCase):
    def setUp(self):
        super().setUp()

    def test_success_register(self):
        data = {
            "phone_number": "09000000001",
            "password": "Salamsalam@123",
            "name": "test_user",
        }
        request = RequestFactory().post(reverse("user_register_mobile"), data=data)
        response = register.RegisterByMobile.as_view()(request)
        assert (
            response.status_code == 201 and response.data["code"] == "register_success"
        )

    def test_duplicated_register(self):
        data = {
            "phone_number": "09000000000",
            "password": "Salamsalam@123",
            "name": "test_user",
        }
        request = RequestFactory().post(reverse("user_register_mobile"), data=data)
        response = register.RegisterByMobile.as_view()(request)
        assert response.status_code == 400 and response.data["code"] == "already_exists"

    def test_invalid_input_register(self):
        data = {
            "phone_number": "090000000000",
            "password": "Salamsalam@123",
            "name": "test_user",
        }
        request = RequestFactory().post(reverse("user_register_mobile"), data=data)
        response = register.RegisterByMobile.as_view()(request)
        assert response.status_code == 400 and response.data["code"] == "invalid_phone"

    def test_weak_password_register(self):
        data = {
            "phone_number": "09000000002",
            "password": "test",
            "name": "test_user",
        }
        request = RequestFactory().post(reverse("user_register_mobile"), data=data)
        response = register.RegisterByMobile.as_view()(request)
        assert response.status_code == 400 and response.data["code"] == "weak_password"
