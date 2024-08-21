from http.client import PROCESSING
from django.db import models

from user.models import User


class Exchange(models.Model):
    ABAN = 1
    BINANCE = 2

    EXCHANGE_TYPES = [
        (ABAN, "aban"),
        (BINANCE, "binance"),
    ]

    name = models.CharField(max_length=25, null=False, unique=True)
    exchange_type = models.IntegerField(choices=EXCHANGE_TYPES, null=False)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Asset(models.Model):

    symbol = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)
    persian_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    trade_fee = models.DecimalField(null=False, max_digits=10, decimal_places=5)
    global_fee = models.DecimalField(null=False, max_digits=10, decimal_places=5)

    def __str__(self):
        return self.symbol


class CryptoAsset(Asset):

    buy = models.BooleanField(default=True)
    sell = models.BooleanField(default=True)
    order_market = models.BooleanField(default=True)
    exchange = models.ForeignKey(
        to=Exchange, on_delete=models.CASCADE, null=False, related_name="coins"
    )


class FiatAsset(Asset):
    is_main = models.BooleanField(default=False)


class StableAsset(CryptoAsset):
    is_main = models.BooleanField(default=False)


class StableAssetPrice(models.Model):
    stable_asset = models.ForeignKey(
        to=StableAsset,
        on_delete=models.CASCADE,
        related_name="price",
        null=False,
    )
    fiat_asset = models.ForeignKey(
        to=FiatAsset,
        on_delete=models.CASCADE,
        related_name="stable_coins",
        null=False,
    )
    price = models.BigIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("stable_asset", "fiat_asset")


class AssetPair(models.Model):
    base_asset = models.ForeignKey(
        to=Asset,
        on_delete=models.CASCADE,
        related_name="quote_assets",
        null=False,
    )
    quote_asset = models.ForeignKey(
        to=Asset,
        on_delete=models.CASCADE,
        related_name="base_assets",
        null=False,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("base_asset", "quote_asset")

    @property
    def symbol(self):
        return f"{self.base_asset.symbol}_{self.quote_asset.symbol}"


class Order(models.Model):
    BUY = 1
    SELL = 2
    SIDES = [
        ("buy", BUY),
        ("sell", SELL),
    ]

    CREATED = 1
    PROCESSING = 2
    FILLED = 3
    SUCCESS = 4
    FAILED = 5
    UNKNOWN = 6

    STATE_CHOICES = [
        ("created", CREATED),
        ("processing", PROCESSING),
        ("filled", FILLED),
        ("success", SUCCESS),
        ("failed", FAILED),
        ("unknown", UNKNOWN),
    ]
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name="orders",
    )
    asset_pair = models.ForeignKey(
        to=AssetPair,
        on_delete=models.CASCADE,
        null=False,
        related_name="orders",
    )
    amount = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    side = models.IntegerField(choices=SIDES, null=False)
    status = models.IntegerField(choices=STATE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ExchangeOrder(models.Model):
    CREATED = 1
    PROCESSING = 2
    SUCCESS = 3
    FAILED = 4
    UNKNOWN = 5
    STATE_CHOICES = [
        ("created", CREATED),
        ("processing", PROCESSING),
        ("success", SUCCESS),
        ("failed", FAILED),
        ("unknown", UNKNOWN),
    ]
    exchange = models.ForeignKey(
        to=Exchange,
        on_delete=models.CASCADE,
        null=False,
        related_name="orders",
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        null=False,
        related_name="exchange_order",
    )
    status = models.IntegerField(choices=STATE_CHOICES, null=False)
    result = models.JSONField(null=True)


class MockOrder(Order):
    WAITING_FOR_MORE = 1
    AGGREGATING = 2
    DONE = 3

    MOCK_STATE = [
        (WAITING_FOR_MORE, "waiting"),
        (AGGREGATING, "aggregating"),
        (DONE, "done"),
    ]

    value = models.DecimalField(max_digits=40, decimal_places=20, null=False)
    mock_status = models.IntegerField(choices=MOCK_STATE, default=WAITING_FOR_MORE)
    aggregated_order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_orders",
    )
