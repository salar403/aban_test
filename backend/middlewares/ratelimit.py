import json

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import caches

from backend.services.ratelimit import check_ip_limit
from backend.settings import DEBUG
from backend.settings.common import BAD_REQUEST_LEVERAGE

cache = caches["default"]


class RateLimitingMiddleware(MiddlewareMixin):

    def response(self, code: str, status: int):
        return HttpResponse(
            content=json.dumps({"code": code}),
            status=status,
            content_type="application/json",
        )

    def process_request(self, request):
        if not DEBUG:
            ip, pseudo_ip, country = self.get_cloudflare_specs(headers=request.headers)
        else:
            ip = request.META.get("REMOTE_ADDR", None)
            pseudo_ip = None
            cdn = None
            country = "LocalHost"
        if not ip:
            return self.response(code="forbidden", status=403)
        if not check_ip_limit(ip=ip):
            return self.response(code="limited", status=429)
        user_agent = request.headers.get("User-Agent", None)
        if not user_agent:
            return self.response(code="invalid_user_agent", status=403)
        request.ip = ip
        request.country = country
        request.device = user_agent
        request.pseudo_ip = pseudo_ip
        request.cdn = cdn

    def process_response(self, request, response):
        if 400 <= response.status_code < 500:
            for _ in range(BAD_REQUEST_LEVERAGE):
                check_ip_limit(ip=request.ip)
        return response

    def get_cloudflare_specs(self, headers):
        ip = headers.get("CF-Connecting-IP", None)
        pseudo_ip = headers.get("Cf-Pseudo-IPv4", None)
        country = headers.get("CF-IPCountry", None)
        return ip, pseudo_ip, country

