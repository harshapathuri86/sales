import datetime
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.forms import ModelForm, HiddenInput, Form, ModelChoiceField, DateField, DateInput

class CounterSelectForm(LoginRequiredMixin, Form):
    counter = ModelChoiceField(queryset=Counter.objects.all())
    date = DateField(initial=datetime.date.today, widget=DateInput(attrs={'type': 'date'}))

class FoodSaleForm(LoginRequiredMixin ,ModelForm):
    class Meta:
        model = FoodSale
        fields = '__all__'
        exclude = ('price',)

    def __init__(self, *args, **kwargs):
        super(FoodSaleForm, self).__init__(*args, **kwargs)

        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['disabled'] = True
        self.fields['date'].widget = HiddenInput()

        self.fields['counter'].widget.attrs['readonly'] = True
        self.fields['counter'].widget.attrs['disabled'] = True
        self.fields['counter'].widget = HiddenInput()
