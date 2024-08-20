import time
from django.core.cache import caches

from backend.settings import (
    REQUEST_RATE_1MIN,
    REQUEST_RATE_15MIN,
    REQUEST_RATE_1HOUR,
    REQUEST_BLOCK_RATE,
)

cache = caches["ratelimit"]


def check_1min(ip: str):
    key = f"{ip}_1m_{time.time()}"
    cache.set(key, True, 60)
    rate = len(cache.keys(f"{ip}_1m_*"))
    return bool(rate <= REQUEST_RATE_1MIN)


def check_15min(ip: str):
    key = f"{ip}_15m_{time.time()}"
    cache.set(key, True, 15 * 60)
    rate = len(cache.keys(f"{ip}_15m_*"))
    return bool(rate <= REQUEST_RATE_15MIN)


def check_1hour(ip: str):
    key = f"{ip}_1h_{time.time()}"
    cache.set(key, True, 60 * 60)
    rate = len(cache.keys(f"{ip}_1h_*"))
    return bool(rate <= REQUEST_RATE_1HOUR)


def check_blocked(ip: str):
    key = f"{ip}_blocked"
    return bool(cache.get(key))


def block_ip_from_backend(ip: str):
    cache.set(f"{ip}_blocked", 1, 60 * 60 * 6)


def check_blocking_limit(ip: str):
    key = f"{ip}_block_{time.time()}"
    cache.set(key, True, 60 * 60)
    rate = len(cache.keys(f"{ip}_block_*"))
    if rate >= REQUEST_BLOCK_RATE:
        block_ip_from_backend(ip=ip)


def check_ip_limit(ip: str):
    if check_blocked(ip):
        return False
    if check_1min(ip) and check_15min(ip) and check_1hour(ip):
        return True
    check_blocking_limit(ip)
    return False
