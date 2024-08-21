from django.db.models.signals import post_save
from django.dispatch import receiver

from exchange.models import MockOrder, Order

from exchange.services.order_manager import MockOrderManager
from exchange.tasks import process_order


@receiver(post_save, sender=MockOrder)
def aggregate_mock_orders(sender, instance, *args, **kwargs):
    try:
        if kwargs["created"]:
            aggregated_order = MockOrderManager().aggregate_orders(order=instance)
            if aggregated_order and isinstance(aggregated_order, Order):
                process_order.apply_async(queue="order", args=(instance.id))
    except Exception as error:
        message = f"exception in new_user signals!! \n {str(error)}"
        # TODO must be logged into log systems
        print(message)
