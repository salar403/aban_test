from decimal import Decimal
from abc import ABC

from exchange.models import Exchange, Order
from exchange.services.outbound_manager import (
    BaseOutboundManager,
    BinanceOutboundManager,
)


class BaseExchangeManager(ABC):

    def __init__(self, exchange: Exchange) -> None:
        self.exchange: Exchange = exchange
        self.outbound: BaseOutboundManager = None

    def submit_market_order(self, asset_symbol: str, amount: Decimal, side: int):
        return self.outbound.submit_market_order(
            pair_symbol=asset_symbol,
            side=dict(map(reversed, dict(Order.SIDES).items()))[side].upper(),
            amount=amount,
        )

    def get_asset_price(self, asset_pair_symbol) -> Decimal:
        return self.outbound(exchange=self.exchange).get_asset_price(
            symbol=asset_pair_symbol
        )


class AbanExchangeManager(BaseExchangeManager):
    pass


class BinanceExchangeManager(BaseExchangeManager):
    def __init__(self, exchange: Exchange) -> None:
        super().__init__(exchange)
        self.outbound = BinanceOutboundManager(exchange=self.exchange)


def get_exchange_manager(excahnge_type: int) -> BaseExchangeManager:
    return {
        Exchange.BINANCE: BinanceExchangeManager,
        Exchange.ABAN: AbanExchangeManager,
    }.get(excahnge_type)
