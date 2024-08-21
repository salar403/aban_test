from decimal import Decimal
from rest_framework import serializers

from exchange.models import AssetPair, Order
from exchange.services.order_manager import OrderRequestManager

from backend.customs.exceptions import CustomException
from backend.customs.utils import get_object_or_none
from exchange.tasks import process_order


class NewMarketOrderSerializer(serializers.Serializer):
    asset_pair = serializers.CharField(required=True)
    amount = serializers.DecimalField(required=True, max_digits=20, decimal_places=10)
    side = serializers.IntegerField(required=True, min_value=1)

    def validate_asset_pair(self, asset_pair):
        if len(asset_pair.split("_")) != 2:
            raise CustomException(code="invalid_asset_pair")
        asset_pair = get_object_or_none(
            AssetPair,
            base_asset__symbol__iexact=asset_pair.split("_")[0],
            quote_asset__symbol__iexact=asset_pair.split("_")[1],
        )
        if not asset_pair:
            raise CustomException(code="invalid_pair")
        if not asset_pair.is_active:
            raise CustomException(code="pair_not_active")
        return asset_pair

    def validate_side(self, side: int):
        if side not in dict(map(reversed, dict(Order.SIDES).items())):
            raise CustomException(code="invalid_side")
        return side

    def validate_amount(self, amount):
        if amount == Decimal(0):
            raise CustomException(code="invalid_amount")
        return Decimal(amount)

    def create(self, validated_data):
        order = OrderRequestManager().create_order(
            user=self.context["request"].client,
            asset_pair=validated_data["asset_pair"],
            amount=validated_data["amount"],
            side=validated_data["side"],
        )
        process_order.apply_async(queue="order", kwargs={"order_id": order.id})
        self._data = {"code": "success", "order_id": order.id}
        return True
