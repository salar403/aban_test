from decimal import Decimal
from django.test import RequestFactory
from django.urls import reverse

from backend.customs.testclasses import UserTestCase, RequestFactory

from exchange.models import Order
from exchange.views import order


class ExchangeOrderServicesTest(UserTestCase):
    def setUp(self):
        super().setUp()

    def test_success_add_sell_order(self):
        data = {
            "asset_pair": "ABAN_USDT",
            "amount": "10",
            "side": 2,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        order_id = response.data["order_id"]
        order_instance = Order.objects.get(id=order_id)
        assert (
            order_instance.side == data["side"]
            and order_instance.amount == Decimal(data["amount"])
            and order_instance.asset_pair.symbol == data["asset_pair"]
        )

    def test_success_add_buy_order(self):
        data = {
            "asset_pair": "ABAN_USDT",
            "amount": "20",
            "side": 1,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        order_id = response.data["order_id"]
        order_instance = Order.objects.get(id=order_id)
        assert (
            order_instance.side == data["side"]
            and order_instance.amount == Decimal(data["amount"])
            and order_instance.asset_pair.symbol == data["asset_pair"]
        )
