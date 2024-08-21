from rest_framework.permissions import BasePermission
from backend.customs.exceptions import CustomException


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, "client", None)
        if not user:
            raise CustomException(code="unauthtenticated", status_code=401)
        return True
