from decimal import Decimal
from django.db import models
from django.db.models.fields import DecimalField
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class ItemPrice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def item_name(self):
        return self.item.name

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # return f"Item Price: {self.item.name} - {self.price} - {self.created_at}"
        return f"{self.price}"


class DailySale(models.Model):
    date = models.DateField(default =  timezone.now, unique=True)

    @property
    def total_sales(self):
        food_sales = FoodSale.objects.filter(date=self)
        return sum([food_sale.sale for food_sale in food_sales])

    def __str__(self):
        return f"{self.date}"


class FoodSale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.ForeignKey(ItemPrice, on_delete=models.CASCADE)
    date = models.ForeignKey(DailySale, on_delete=models.CASCADE)
    prepared_quantity = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    leftover_quantity = models.DecimalField(max_digits=5, decimal_places=3, default=0)

    @property
    def sale(self):
        return (self.prepared_quantity - self.leftover_quantity)*10*self.price.price

    def save(self, *args, **kwargs):
        self.price = ItemPrice.objects.filter(item=self.item).first()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Food sale {self.item} - {self.date}"
