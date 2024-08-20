from django.db import models


class Exchange(models.Model):
    BINANCE = 1

    EXCHANGE_TYPES = [
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
