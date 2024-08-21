from decimal import Decimal
from django.test import TestCase
from django.test import RequestFactory as BaseRequestFactory

import exchange
from user.models import User
from exchange.models import AssetPair, CryptoAsset, Exchange, FiatAsset, StableAsset


class ExchangeTestCase(TestCase):
    def setUp(self):
        self.exchange = Exchange.objects.create(
            name="test_exchange",
            exchange_type=Exchange.BINANCE,
        )


class AssetTestCase(ExchangeTestCase):
    def setUp(self):
        super().setUp()
        self.base_asset = CryptoAsset.objects.create(
            symbol="ABAN",
            name="aban token",
            persian_name="توکن آبان",
        )
        self.quote_asset = StableAsset.objects.create(
            symbol="USDT",
            name="tether",
            persian_name="تتر",
            is_main=True,
        )
        self.fiat_asset = FiatAsset.objects.create(
            symbol="IRT",
            name="TOMAN",
            persian_name="تومان",
            is_main=True,
        )
        self.asset_pair = AssetPair.objects.create(
            base_asset=self.base_asset,
            quote_asset=self.quote_asset,
            exchange=self.exchange,
            min_order_value=Decimal(10),
        )


class UserTestCase(AssetTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(phone_number="09000000000", name="test user")
        self.user.set_password(password="Salamsalam@123")


class RequestFactory(BaseRequestFactory):
    def get(self, path, data=None, secure=False, **extra):
        request = super().get(path, data, secure, **extra)
        request.ip = "1.2.3.4"
        request.pseudo_ip = None
        request.device = "test_device"
        request.country = "NA"
        return request

    def post(
        self, path, data=None, content_type="application/json", secure=False, **extra
    ):
        request = super().post(path, data, content_type, secure, **extra)
        request.ip = "1.2.3.4"
        request.pseudo_ip = None
        request.device = "test_device"
        request.country = "NA"
        return request

    def put(
        self,
        path,
        data="",
        content_type="application/json",
        secure=False,
        **extra,
    ):
        request = super().put(path, data, content_type, secure, **extra)
        request.ip = "1.2.3.4"
        request.pseudo_ip = None
        request.device = "test_device"
        request.country = "NA"
        return request

    def delete(
        self,
        path,
        data="",
        content_type="application/json",
        secure=False,
        **extra,
    ):
        request = super().delete(path, data, content_type, secure, **extra)
        request.ip = "1.2.3.4"
        request.pseudo_ip = None
        request.device = "test_device"
        request.country = "NA"
        return request
