from backend import settings
from django.urls import path, re_path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.contrib.staticfiles.views import serve


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


schema_view = get_schema_view(
    openapi.Info(
        title="Aban Test",
        default_version="v1.0",
        description="Aban Test API",
        contact=openapi.Contact(email="salar40340@gmail.com"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=settings.SWAGGER_SETTINGS["DEFAULT_API_URL"],
)

urlpatterns = [
    path(
        "jkc3Em1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("user/", include("user.urls")),
    path("exchange/", include("exchange.urls")),
    re_path(r"^static/(?P<path>.*)$", return_static, name="static"),  #  add this line
]
