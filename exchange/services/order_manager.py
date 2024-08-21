from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from accounting.models import Portfo
from backend.customs.exceptions import CustomException
from exchange.models import AssetPair, Exchange, ExchangeOrder, MockOrder, Order
from accounting.services.portfo_manager import PortfoManager
from exchange.services.exchange_manager import BaseExchangeManager, get_exchange_manager
from user.models import SystemUser, User


class BaseOrderManager:
    def __init__(self) -> None:
        self.base_portfo: Portfo = None
        self.quote_portfo: Portfo = None
        self.asset_pair: AssetPair = None
        self.user: User = None
        self.price: Decimal = None
        self.amount: Decimal = None
        self.value: Decimal = None
        self.side: int = None
        self.exchange_manager: BaseExchangeManager = None
        self.exchange: Exchange = None

    def setup_portfo(self):
        self.base_portfo = PortfoManager.get_portfo(
            user=self.user, asset=self.asset_pair.base_asset
        )
        self.quote_portfo = PortfoManager.get_portfo(
            user=self.user, asset=self.asset_pair.quote_asset
        )

    def setup_exchange(self) -> Exchange:
        self.exchange = self.asset_pair.exchange
        self.exchange_manager = get_exchange_manager(
            excahnge_type=self.exchange.exchange_type
        )

    def predict_order_value(self):
        self.price = self.exchange_manager(
            exchange=self.asset_pair.exchange
        ).get_asset_price(asset_pair_symbol=self.asset_pair.symbol)
        self.value = self.price * self.amount

    def block_portfo(self):
        if self.side == Order.BUY:
            PortfoManager(portfo=self.quote_portfo).block_balance(
                amount=self.value, description="blockd for buy order"
            )
        else:
            PortfoManager(portfo=self.base_portfo).block_balance(
                amount=self.amount, description="blockd for sell order"
            )


class OrderRequestManager(BaseOrderManager):

    def create_order(
        self,
        user: User,
        asset_pair: AssetPair,
        amount: Decimal,
        side: int,
    ):
        self.user = user
        self.asset_pair = asset_pair
        self.amount = amount
        self.side = side
        with transaction.atomic():
            self.setup_portfo()
            self.setup_exchange()
            self.predict_order_value()
            self.block_portfo()
            return Order.objects.create(
                user=user,
                asset_pair=asset_pair,
                amount=amount,
                side=side,
            )


class OrderManager(BaseOrderManager):
    def __init__(self) -> None:
        super().__init__()
        self.order = None

    def mock_order(self):
        MockOrder.objects.create(order=self.order, value=self.value)
        return {}

    def create_exchange_order(self, result: dict):
        ExchangeOrder.objects.create(
            exchange=self.exchange,
            order=self.order,
            status=ExchangeOrder.SUCCESS,
            result=result,
        )

    def add_balance(self):
        if self.order.side == Order.SELL:
            PortfoManager(portfo=self.quote_portfo).add_balance(
                amount=self.value, description="added for sell order"
            )
        else:
            PortfoManager(portfo=self.base_portfo).add_balance(
                amount=self.value / self.order.amount, description="added for buy order"
            )

    def release_blocked(self):
        if self.order.side == Order.SELL:
            PortfoManager(portfo=self.base_portfo).remove_blocked(
                amount=self.order.amount,
                description="remobed after sell order",
            )
        else:
            PortfoManager(portfo=self.quote_portfo).remove_blocked(
                amount=self.value,
                allow_negative=True,
                description="removed affter buy order",
            )

    def process_order(self, order: Order):
        self.order = order
        self.user = order.user
        self.asset_pair = order.asset_pair
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=self.order.id)
            if order.status != Order.PROCESSING:
                raise CustomException(code="invalid_order_state")
            self.setup_portfo()
            self.setup_exchange()
            self.predict_order_value()
            self.block_portfo()
            if self.value >= self.order.asset_pair.min_order_value:
                result = self.exchange_manager.submit_market_order(
                    asset_symbol=self.order.asset_pair.symbol,
                    amount=self.order.amount,
                    side=self.order.side,
                )
                self.value = result["value"]
                self.create_exchange_order(result=result)
            else:
                self.mock_order()
            self.add_balance()
            self.release_blocked()
            order.status = Order.SUCCESS
            order.save()


class MockOrderManager(BaseOrderManager):
    def __init__(self) -> None:
        super().__init__()
        self.aggregated_order = None

    def create_aggregated_order(self):
        self.aggregated_order = Order.objects.create(
            user=SystemUser.object().user,
            asset_pair=self.asset_pair,
            amount=self.amount if self.side == MockOrder.SELL else self.value,
            side=self.side,
        )

    def aggregate_orders(self, order: MockOrder):
        self.asset_pair = order.asset_pair
        self.side = order.side
        with transaction.atomic():
            waiting_mock_orders = MockOrder.objects.select_for_update().filter(
                asset_pair=order.asset_pair,
                mock_state=MockOrder.WAITING_FOR_MORE,
                side=MockOrder.side,
            )
            aggregated_data = waiting_mock_orders.aggregate(
                sum_amount=Sum("amount"), sum_value=Sum("value")
            )
            self.amount = aggregated_data["sum_amount"]
            self.value = aggregated_data["sum_value"]
            self.predict_order_value()
            if self.value >= self.asset_pair.min_order_value:
                self.create_aggregated_order()
                for order in waiting_mock_orders:
                    order.mock_state = MockOrder.DONE
                    order.aggregated_order = self.aggregated_order
                    order.save()
                return self.aggregated_order
