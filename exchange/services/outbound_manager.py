from abc import ABC, abstractclassmethod
from decimal import Decimal
from django.core.cache import caches

import requests

from exchange.models import Exchange

price_cache = caches["coin_info"]


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
        try:
            result = requests.request(
                method=method,
                url=f"{self.BASE_URL}{url}",
                params=params,
                headers=headers,
                body=body,
                timeout=timeout,
            )
            return {"success": True, "code": result.status_code, "data": result.json()}
        except Exception as error:
            return {"success": False, "error": str(error)}

    def get_asset_price(self, symbol: str):
        return Decimal(str(price_cache.get(f"price_{symbol}")))

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
