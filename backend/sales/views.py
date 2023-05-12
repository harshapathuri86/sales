from rest_framework import viewsets, status
from rest_framework.routers import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.http import Http404
from .models import *
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from django_filters.rest_framework import DjangoFilterBackend

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

