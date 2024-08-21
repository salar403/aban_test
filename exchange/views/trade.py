from rest_framework import status

from backend.customs.views import CreateApiView

from backend.customs.permissions import IsAuthenticated
from exchange.serializers.trade import NewMarketOrderSerializer


class NewMarketOrder(CreateApiView):
    parser_classes = [IsAuthenticated]
    serializer_class = NewMarketOrderSerializer
    context_map = {"request": None}
    response_code = status.HTTP_201_CREATED
