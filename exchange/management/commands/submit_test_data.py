from decimal import Decimal
from django.core.management.base import BaseCommand
from exchange.models import (
    AssetPair,
    CryptoAsset,
    Exchange,
    FiatAsset,
    StableAsset,
    StableAssetPrice,
)
from user.models import SystemUser


class Command(BaseCommand):
    help = "this command creates needed objects for first time running project"

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        binance = Exchange.objects.create(
            name="binance test",
            exchange_type=Exchange.BINANCE,
        )
        aban = Exchange.objects.create(
            name="Aban",
            exchange_type=Exchange.ABAN,
        )
        aban_token = CryptoAsset.objects.create(
            symbol="ABAN", name="aban token", persian_name="توکن أبان"
        )
        usdt = StableAsset.objects.create(
            symbol="USDT", name="tether", persian_name="تتر", is_main=True
        )
        irt = FiatAsset.objects.create(
            symbol="IRT", name="toman", persian_name="تومان", is_main=True
        )
        usdt_price = StableAssetPrice(
            stable_asset=usdt, fiat_asset=irt, price=Decimal(60000)
        )
        system_user = SystemUser.objects.create(
            name="aban", phone_number="00000000000", password=None
        )
        asset_pair = AssetPair.objects.create(
            base_asset=aban_token,
            quote_asset=usdt,
            exchange=binance,
            min_order_value=Decimal(10),
        )

        self.stdout.write(self.style.SUCCESS("Successfully created basic data"))
