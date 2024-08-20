import json
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.core.cache import caches

from backend.customs.decorators import locked_process

coin_info_cache = caches["coin_info"]


@shared_task
@locked_process(expire_time=3)
def update_coin_price(price_map: dict):
    return price_map


def get_or_set_websocket_price():
    return {}


@shared_task
@locked_process(expire_time=5 * 60)
def send_socket_price():
    channel_layer = get_channel_layer()
    price_map = get_or_set_websocket_price()
    async_to_sync(channel_layer.group_send)(
        "coins_data",
        {
            "type": "send_price",
            "data": json.dumps(price_map),
        },
    )
