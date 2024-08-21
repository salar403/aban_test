from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

from exchange.models import Asset
from user.models import User
from accounting.services.portfo_manager import PortfoManager


@receiver(post_save, sender=User)
def increase_new_user_balance(sender, instance, *args, **kwargs):
    try:
        if kwargs["created"]:
            base_portfo = PortfoManager.get_portfo(user=instance, asset=Asset.objects.get(symbol="ABAN"))
            quote_portfo = PortfoManager.get_portfo(user=instance, asset=Asset.objects.get(symbol="USDT"))
            PortfoManager(portfo=base_portfo).add_balance(amount=Decimal("100000"), description="register gift")
            PortfoManager(portfo=quote_portfo).add_balance(amount=Decimal("100000"), description="register gift")
    except Exception as error:
        message = f"exception in new_user signals!! \n {str(error)}"
        # TODO must be logged into log systems
        print(message)
