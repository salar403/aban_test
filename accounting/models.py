from django.db import models

from exchange.models import Asset
from user.models import User


class Portfo(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name="portfo",
    )
    asset = models.ForeignKey(
        to=Asset,
        on_delete=models.CASCADE,
        null=False,
        related_name="owners",
    )
    balance = models.DecimalField(
        max_digits=40,
        decimal_places=20,
        default=0,
        null=False,
    )
    blocked = models.DecimalField(
        max_digits=40,
        decimal_places=20,
        default=0,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "asset")


class Transaction(models.Model):
    portfo = models.ForeignKey(
        to=Portfo,
        on_delete=models.CASCADE,
        null=False,
        related_name="transactions",
    )
    start_balance = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    balance_change = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    end_balance = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    start_blocked = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    blocked_change = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    end_blocked = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
