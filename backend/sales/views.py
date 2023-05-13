from rest_framework import viewsets, status
from rest_framework.routers import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.http import Http404
from .models import *
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
# from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, DetailView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404, redirect, render

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, format = None):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response({'items': serializer.data}, template_name='sales/item/item_list.html')

    def retrieve(self, request, pk=None, format = None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response({'item': serializer.data}, template_name='sales/item/item.html')

    def create(self, request, format = None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'item': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, format = None):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'item': serializer.data}, template_name='sales/item/item.html')

    def destroy(self, request, pk=None, format = None):
        print('delete', pk)
        item = Item.objects.get(pk=pk)
        item.delete()
        return redirect('item-list')

class ItemPriceViewSet(viewsets.ModelViewSet):
    queryset = ItemPrice.objects.all()
    serializer_class = ItemPriceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, format = None):
        queryset = ItemPrice.objects.all()
        serializer = ItemPriceSerializer(queryset, many=True)
        item_prices = []
        for item_price in serializer.data:
            item = Item.objects.get(pk=item_price['item'])
            item_price['item_name'] = item.name
            item_prices.append(item_price)
        return Response({'itemprices': item_prices}, template_name='sales/itemprice/itemprice_list.html')

    def retrieve(self, request, pk=None, format = None):
        queryset = ItemPrice.objects.all()
        itemprice = get_object_or_404(queryset, pk=pk)
        serializer = ItemPriceSerializer(itemprice)
        item_name = itemprice.item_name
        return Response({
            'itemprice': serializer.data,
            'item_name': item_name
         }, template_name='sales/itemprice/itemprice.html')

    def create(self, request, format = None):
        serializer = ItemPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'itemprice': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST, template_name='40x.html')

    def update(self, request, pk=None, format = None):
        itemprice = ItemPrice.objects.get(pk=pk)
        item_name = itemprice.item_name
        serializer = ItemPriceSerializer(itemprice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("data", serializer.data)
            return Response({
                'itemprice': serializer.data, 
                'item_name': item_name
                             }, template_name='sales/itemprice/itemprice.html')
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST, template_name='40x.html')

    def destroy(self, request, pk=None, format = None):
        itemprice = ItemPrice.objects.get(pk=pk)
        itemprice.delete()
        return redirect('itemprice-list')

