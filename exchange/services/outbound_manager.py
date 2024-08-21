from abc import ABC, abstractclassmethod
from decimal import Decimal

from exchange.models import Exchange


class BaseOutboundManager(ABC):
    BASE_URL = None

    def __init__(self, exchange: Exchange) -> None:
        self.exchange = exchange
        self.base_url = self.BASE_URL

    def send(
        self,
        method: str,
        url: str,
        params: dict = None,
        headers: dict = None,
        body: dict = None,
        timeout: int = 30,
    ):
        # send to outbound
        pass

    def get_asset_price(self, symbol: str):
        return Decimal(4)

    @abstractclassmethod
    def submit_market_order(self, pair_symbol: str, side: str, amount: Decimal) -> dict:
        pass


class BinanceOutboundManager(BaseOutboundManager):

    def submit_market_order(self, pair_symbol: str, side: str, amount: Decimal) -> dict:
        price = self.get_asset_price(symbol=pair_symbol)
        base_amount = amount
        quote_amount = amount * Decimal(str(price))
        return {
            "pair_symbol": pair_symbol,
            "price": str(price),
            "side": side,
            "value": str(quote_amount),
            "base_amount": str(base_amount),
            "quote_amount": str(quote_amount),
        }
