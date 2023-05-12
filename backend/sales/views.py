from rest_framework import viewsets
from .models import *
from .serializers import *

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemPriceViewSet(viewsets.ModelViewSet):
    queryset = ItemPrice.objects.all()
    serializer_class = ItemPriceSerializer

class DailySaleViewSet(viewsets.ModelViewSet):
    queryset = DailySale.objects.all()
    serializer_class = DailySaleSerializer

class FoodSaleViewSet(viewsets.ModelViewSet):
    queryset = FoodSale.objects.all()
    serializer_class = FoodSaleSerializer
