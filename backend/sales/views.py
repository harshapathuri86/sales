from rest_framework import viewsets, status
from rest_framework.routers import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.http import Http404
from .models import *
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
# from django_filters.rest_framework import DjangoFilterBackend

# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#
# class ItemPriceViewSet(viewsets.ModelViewSet):
#     queryset = ItemPrice.objects.all()
#     serializer_class = ItemPriceSerializer
#
# class DailySaleViewSet(viewsets.ModelViewSet):
#     queryset = DailySale.objects.all()
#     serializer_class = DailySaleSerializer
#
# class FoodSaleViewSet(viewsets.ModelViewSet):
#     queryset = FoodSale.objects.all()
#     serializer_class = FoodSaleSerializer


class ItemList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sales/item_list.html'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        items = Item.objects.all()
        return Response({'items': items})

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemDetail(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sales/item.html'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, itemId):
        try:
            return Item.objects.get(id=itemId)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, itemId, format=None):
        item = self.get_object(itemId)
        serializer = ItemSerializer(item)
        return Response({'item': item})

    def put(self, request, itemId, format=None):
        item = self.get_object(itemId)
        serializer = ItemSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, itemId, format=None):
        item = self.get_object(itemId)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemPriceList(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        queryset = ItemPrice.objects.all()
        data = ItemPriceSerializer(queryset, many=True).data
        return Response(data)

    def post(self, request, format=None):
        serializer = ItemPriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ItemPriceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, itemPriceId):
        try:
            return ItemPrice.objects.get(id=itemPriceId)
        except ItemPrice.DoesNotExist:
            raise Http404

    def get(self, request, itemPriceId, format=None):
        item = self.get_object(itemPriceId)
        serializer = ItemPriceSerializer(item)
        return Response(serializer.data)

    def put(self, request, itemPriceId, format=None):
        item = self.get_object(itemPriceId)
        serializer = ItemPriceSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, itemPriceId, format=None):
        item = self.get_object(itemPriceId)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DailySaleList(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        queryset = DailySale.objects.all()
        data = DailySaleSerializer(queryset, many=True).data
        return Response(data)

    def post(self, request, format=None):
        serializer = DailySaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DailySaleDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, dailySaleId):
        try:
            return DailySale.objects.get(id=dailySaleId)
        except DailySale.DoesNotExist:
            raise Http404

    def get(self, request, dailySaleId, format=None):
        item = self.get_object(dailySaleId)
        serializer = DailySaleSerializer(item)
        return Response(serializer.data)

    def put(self, request, dailySaleId, format=None):
        item = self.get_object(dailySaleId)
        serializer = DailySaleSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, dailySaleId, format=None):
        item = self.get_object(dailySaleId)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FoodSaleList(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        queryset = FoodSale.objects.all()
        data = FoodSaleSerializer(queryset, many=True).data
        return Response(data)

    def post(self, request, format=None):
        serializer = FoodSaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FoodSaleDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, foodSaleId):
        try:
            return FoodSale.objects.get(id=foodSaleId)
        except FoodSale.DoesNotExist:
            raise Http404

    def get(self, request, foodSaleId, format=None):
        item = self.get_object(foodSaleId)
        serializer = FoodSaleSerializer(item)
        return Response(serializer.data)

    def put(self, request, foodSaleId, format=None):
        item = self.get_object(foodSaleId)
        serializer = FoodSaleSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, foodSaleId, format=None):
        item = self.get_object(foodSaleId)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

