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
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=3)


    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be less than zero.")
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name

class FoodSale(models.Model):
    
    class Meta:
        ordering = ['-date', 'counter', 'item']
        indexes = [
            models.Index(fields=['counter']),
            models.Index(fields=['item']),
            models.Index(fields=['date', 'counter', 'item']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['item', 'date', 'counter'], name='unique_food_sale'),
        ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    price = models.DecimalField(max_digits=5, decimal_places=3)
    outgoing = models.IntegerField()
    incoming = models.IntegerField()

    def clean(self):
        if self.outgoing < 0:
            raise ValidationError("Outgoing quantity cannot be less than zero.")
        if self.incoming < 0:
            raise ValidationError("Incoming quantity cannot be less than zero.")
        if self.incoming > self.outgoing:
            raise ValidationError("Incoming quantity cannot be greater than prepared quantity.")

    @property
    def sold_quantity(self):
        return (self.outgoing - self.incoming)

    @property
    def sale(self):
        return (self.outgoing - self.incoming)*self.price

    def save(self, *args, **kwargs):
        self.price = self.item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Food sale {self.item} - {self.counter} - {self.date}"
