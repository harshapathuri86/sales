from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Counter(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be less than zero.")
        self.name = self.name.capitalize()

    def __str__(self):
        # return f"{self.name} - {self.price}"
        return self.name

class DailySale(models.Model):
    date = models.DateField(default =  timezone.now, unique=True)

    @property
    def total_sales(self):
        food_sales = FoodSale.objects.filter(date=self)
        return sum([food_sale.sale for food_sale in food_sales])

    def __str__(self):
        # return f"{self.date}"
        return self.date.strftime('%B %d, %Y')


class FoodSale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    date = models.ForeignKey(DailySale, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    prepared_quantity = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    leftover_quantity = models.DecimalField(max_digits=5, decimal_places=3, default=0)

    def clean(self):
        if self.prepared_quantity < 0:
            raise ValidationError("Prepared quantity cannot be less than zero.")
        if self.leftover_quantity < 0:
            raise ValidationError("Leftover quantity cannot be less than zero.")
        if self.leftover_quantity > self.prepared_quantity:
            raise ValidationError("Leftover quantity cannot be greater than prepared quantity.")

    # def validate_unique(self, exclude=None):
    #     qs = FoodSale.objects.filter(item=self.item, date=self.date, counter=self.counter)
    #     if qs.exists():
    #         raise ValidationError('Food sale for this item, counter and date already exists')
    #
    @property
    def sold_quantity(self):
        return (self.prepared_quantity - self.leftover_quantity)

    @property
    def sale(self):
        return (self.prepared_quantity - self.leftover_quantity)*10*self.price

    def save(self, *args, **kwargs):
        self.price = self.item.price
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Food sale {self.item} - {self.counter} - {self.date}"
