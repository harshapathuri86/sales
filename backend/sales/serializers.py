from django.db.models.expressions import fields
from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = '__all__'

class DailySaleSerializer(serializers.ModelSerializer):

    total_sales = serializers.SerializerMethodField()

    class Meta:
        model = DailySale
        fields = '__all__'

    def get_total_sales(self, obj):
        return obj.total_sales


class FoodSaleSerializer(serializers.ModelSerializer):

    sale = serializers.SerializerMethodField()

    class Meta:
        model = FoodSale
        fields = '__all__'
        extra_kwargs = {
            'prepared_quantity': {'required': True, 'min_value': 0},
            'leftover_quantity': {'required': True, 'min_value': 0},
        }

    def get_sale(self, obj):
        return obj.sale

    def validate(self, attrs):
        prepared_quantity = attrs.get('prepared_quantity')
        leftover_quantity = attrs.get('leftover_quantity')

        if prepared_quantity and leftover_quantity:
            if leftover_quantity > prepared_quantity:
                raise serializers.ValidationError("Leftover quantity cannot be greater than prepared quantity.")

        return attrs
