from django.test import RequestFactory
from django.urls import reverse

from backend.customs.testclasses import UserTestCase, RequestFactory

from exchange.views import order


class ExchangeOrderViewsTest(UserTestCase):
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
        assert (
            response.status_code == 201
            and response.data["code"] == "success"
            and "order_id" in response.data
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
        assert (
            response.status_code == 201
            and response.data["code"] == "success"
            and "order_id" in response.data
        )


    def test_fail_order_balance(self):
        data = {
            "asset_pair": "ABAN_USDT",
            "amount": 999999999,
            "side": 2,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        assert (
            response.status_code == 400
            and response.data["code"] == "insufficient_balance"
        )

    def test_fail_order_wrong_pair_format(self):
        data = {
            "asset_pair": "ABAN_USDT_9",
            "amount": 10,
            "side": 2,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        assert (
            response.status_code == 400
            and response.data["code"] == "invalid_asset_pair"
        )

    def test_fail_order_wrong_pair(self):
        data = {
            "asset_pair": "ABAN_SHITCOIN",
            "amount": 10,
            "side": 2,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        assert response.status_code == 400 and response.data["code"] == "invalid_pair"

    def test_fail_order_wrong_side(self):
        data = {
            "asset_pair": "ABAN_USDT",
            "amount": 10,
            "side": 3,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        assert response.status_code == 400 and response.data["code"] == "invalid_side"

    def test_fail_order_zero_amount(self):
        data = {
            "asset_pair": "ABAN_USDT",
            "amount": 0,
            "side": 2,
        }
        request = RequestFactory().post(reverse("new_market_order"), data=data)
        request.client = self.user
        response = order.NewMarketOrder.as_view()(request)
        assert response.status_code == 400 and response.data["code"] == "invalid_amount"
