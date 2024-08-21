from django.urls import path
from exchange.views import order

urlpatterns = [
    path("trde/market/", order.NewMarketOrder.as_view(), name="new_market_order"),
]
