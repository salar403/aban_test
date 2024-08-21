from decimal import Decimal
from django.test import RequestFactory
from django.urls import reverse

from accounting.models import Portfo
from accounting.services.portfo_manager import PortfoManager
from backend.customs.exceptions import InsufficientBalance, InsufficientBlocked
from backend.customs.testclasses import UserTestCase, RequestFactory

from user.views import auth


class AccountingServiceTestCase(UserTestCase):
    def setUp(self):
        super().setUp()

    def test_get_portfo(self):
        base_portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        quote_portfo = PortfoManager.get_portfo(user=self.user, asset=self.quote_asset)
        assert isinstance(base_portfo, Portfo) and isinstance(quote_portfo, Portfo)

    def test_add_balance(self):
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        current_balance = portfo.balance
        PortfoManager(portfo=portfo).add_balance(
            amount=Decimal(10), description="test payment"
        )
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        assert portfo.balance == Decimal(10) + current_balance

    def test_block_balance_success(self):
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        current_balance = portfo.balance
        current_blocked = portfo.blocked
        PortfoManager(portfo=portfo).block_balance(
            amount=portfo.balance - Decimal(10), description="test payment"
        )
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        assert portfo.balance == Decimal(
            10
        ) and portfo.blocked == current_blocked + current_balance - Decimal(10)

    def test_block_balance_fail(self):
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        try:
            PortfoManager(portfo=portfo).block_balance(
                amount=portfo.balance + Decimal(10), description="test payment"
            )
        except InsufficientBalance:
            assert True
        else:
            assert False

    def test_remove_blocked_success(self):
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        portfo.blocked += Decimal(10)
        portfo.save()
        PortfoManager(portfo=portfo).remove_blocked(
            amount=portfo.blocked, description="test payment"
        )
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        assert portfo.blocked == Decimal(0)

    def test_remove_blocked_fail(self):
        portfo = PortfoManager.get_portfo(user=self.user, asset=self.base_asset)
        portfo.blocked += Decimal(10)
        portfo.save()
        try:
            PortfoManager(portfo=portfo).remove_blocked(
                amount=portfo.blocked + Decimal(10), description="test payment"
            )
        except InsufficientBlocked:
            assert True
        else:
            assert False
