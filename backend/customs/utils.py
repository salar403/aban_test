from django.forms import model_to_dict
from rest_framework import serializers

from backend.customs.exceptions import CustomException


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True, allow_null=False)
    per_page = serializers.IntegerField(required=True, allow_null=False)


def custom_paginator(queryset: list, serializer_data: dict):
    page = serializer_data["page"]
    per_page = serializer_data["per_page"]
    return queryset[(page - 1) * per_page : page * per_page]


def paginated_queryset(Class, query_page: int = 1, query_per_page: int = 10, **kwargs):
    start_place = (query_page - 1) * query_per_page
    end_place = query_page * query_per_page
    if hasattr(Class, "_default_manager"):
        class_manager = Class._default_manager
    else:
        class_manager = Class
    return class_manager.filter(**kwargs)[start_place:end_place]


def detailed_paginated_queryset(
    Class, query_page: int = 1, query_per_page: int = 10, **kwargs
):
    start_place = (query_page - 1) * query_per_page
    end_place = query_page * query_per_page
    if hasattr(Class, "_default_manager"):
        class_manager = Class._default_manager
    else:
        class_manager = Class
    object_count = class_manager.filter(**kwargs).count()
    queryset = class_manager.filter(**kwargs)[start_place:end_place]
    return {
        "page": query_page,
        "per_page": query_per_page,
        "total": object_count,
        "queryset": queryset,
    }


def get_object_or_false(Class, *args, **kwargs):
    queryset = (
        Class._default_manager.all() if hasattr(Class, "_default_manager") else Class
    )
    try:
        return [queryset.get(*args, **kwargs), True]
    except queryset.model.DoesNotExist:
        return [None, False]


def get_object_or_none(Class, *args, **kwargs):
    queryset = (
        Class._default_manager.all() if hasattr(Class, "_default_manager") else Class
    )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_object_or_404(Class, *args, **kwargs):
    instance = get_object_or_none(Class, *args, **kwargs)
    if not instance:
        raise CustomException(code="not_found", status_code=404)
    return instance


def bulk_model_to_dict(queryset, fields=None, exclude=None):
    result = []
    for item in queryset:
        result.append(model_to_dict(instance=item, fields=fields, exclude=exclude))
    return result
