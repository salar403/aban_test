from celery import shared_task
from django.db import transaction

from backend.customs.decorators import locked_process
from exchange.models import Order
from exchange.services.order_manager import OrderManager


@shared_task
@locked_process(expire_time=5 * 60)
def process_order(order_id: int):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id, status=Order.CREATED)
        order.status = Order.PROCESSING
        order.save()
        OrderManager().process_order(order=order)
