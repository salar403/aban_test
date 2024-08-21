from decimal import Decimal
from django.db import transaction

from accounting.models import Portfo, Transaction
from backend.customs.exceptions import InsufficientBalance, InsufficientBlocked
from exchange.models import Asset
from user.models import User


class PortfoManager:
    def __init__(self, portfo: Portfo):
        self.portfo = portfo

    def create_transaction(
        self,
        portfo: Portfo,
        start_balance: Decimal = Decimal(0),
        balance_change: Decimal = Decimal(0),
        end_balance: Decimal = Decimal(0),
        start_blocked: Decimal = Decimal(0),
        blocked_change: Decimal = Decimal(0),
        end_blocked: Decimal = Decimal(0),
        description: str = None,
    ):
        Transaction.objects.create(
            portfo=portfo,
            start_balance=start_balance,
            balance_change=balance_change,
            end_balance=end_balance,
            start_blocked=start_blocked,
            blocked_change=blocked_change,
            end_blocked=end_blocked,
            description=description,
        )

    def block_balance(
        self, amount: Decimal, description: str, allow_negative: bool = False
    ):
        with transaction.atomic():
            portfo = Portfo.objects.select_for_update().get(id=self.portfo.id)
            if portfo.balance - amount < 0 and not allow_negative:
                raise InsufficientBalance()
            self.create_transaction(
                portfo=portfo,
                start_balance=portfo.balance,
                balance_change=-1 * amount,
                end_balance=portfo.balance - amount,
                start_blocked=portfo.blocked,
                blocked_change=amount,
                end_blocked=portfo.blocked + amount,
                description=description,
            )
            portfo.balance -= amount
            portfo.blocked += amount
            portfo.save()

    def add_balance(self, amount: Decimal, description: str):
        with transaction.atomic():
            portfo = Portfo.objects.select_for_update().get(id=self.portfo.id)
            self.create_transaction(
                portfo=portfo,
                start_balance=portfo.balance,
                balance_change=amount,
                end_balance=portfo.balance + amount,
                description=description,
            )
            portfo.balance += amount
            portfo.save()

    def remove_blocked(
        self, amount: Decimal, description: str, allow_negative: bool = False
    ):
        with transaction.atomic():
            portfo = Portfo.objects.select_for_update().get(id=self.portfo.id)
            self.create_transaction(
                portfo=portfo,
                start_blocked=portfo.blocked,
                blocked_change=-1 * amount,
                end_blocked=portfo.blocked - amount,
                description=description,
            )
            portfo.blocked -= amount
            if portfo.blocked < 0 and not allow_negative:
                raise InsufficientBlocked()
            portfo.save()

    @staticmethod
    def get_portfo(user: User, asset: Asset):
        portfo, created = Portfo.objects.get_or_create(user=user, asset=asset)
        return portfo
