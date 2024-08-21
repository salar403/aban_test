from django.db.models.signals import post_save
from django.dispatch import receiver

from exchange.models import MockOrder, Order

from exchange.services.order_manager import MockOrderManager
from exchange.tasks import process_order


@receiver(post_save, sender=MockOrder)
def aggregate_mock_orders(sender, instance, *args, **kwargs):

    if kwargs["created"]:
        aggregated_order = MockOrderManager().aggregate_orders(order=instance)
        if aggregated_order and isinstance(aggregated_order, Order):
            process_order.apply_async(
                queue="order", kwargs={"order_id": aggregated_order.id}
            )
