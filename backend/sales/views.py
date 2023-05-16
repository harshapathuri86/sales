import datetime
from .models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

class ItemListView(ListView):
    model = Item
    template_name = 'sales/item/item_list.html'
    context_object_name = 'items'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'sales/item/item.html'
    context_object_name = 'item'

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'sales/item/item_create.html'
    fields = '__all__'
    success_url = reverse_lazy('item-list')

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'sales/item/item_update.html'
    fields = '__all__'
    success_url = reverse_lazy('item-list')

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'sales/item/item_delete.html'
    success_url = reverse_lazy('item-list')

class CounterListView(ListView):
    model = Counter
    template_name = 'sales/counter/counter_list.html'
    context_object_name = 'counters'

class CounterDetailView(DetailView):
    model = Counter
    template_name = 'sales/counter/counter.html'
    context_object_name = 'counter'

class CounterCreateView(LoginRequiredMixin, CreateView):
    model = Counter
    template_name = 'sales/counter/counter_create.html'
    fields = '__all__'
    success_url = reverse_lazy('counter-list')

class CounterUpdateView(LoginRequiredMixin, UpdateView):
    model = Counter
    template_name = 'sales/counter/counter_update.html'
    fields = '__all__'
    success_url = reverse_lazy('counter-list')

class CounterDeleteView(LoginRequiredMixin, DeleteView):
    model = Counter
    template_name = 'sales/counter/counter_delete.html'
    success_url = reverse_lazy('counter-list')

class DailySaleListView(ListView):
    model = DailySale
    template_name = 'sales/dailysale/dailysale_list.html'
    context_object_name = 'dailysales'

class DailySaleDetailView(DetailView):
    model = DailySale
    template_name = 'sales/dailysale/dailysale.html'
    context_object_name = 'dailysale'

class DailySaleCreateView(LoginRequiredMixin, CreateView):
    model = DailySale
    template_name = 'sales/dailysale/dailysale_create.html'
    fields = '__all__'
    success_url = reverse_lazy('dailysale-list')

class DailySaleUpdateView(LoginRequiredMixin, UpdateView):
    model = DailySale
    template_name = 'sales/dailysale/dailysale_update.html'
    fields = '__all__'
    success_url = reverse_lazy('dailysale-list')

class DailySaleDeleteView(LoginRequiredMixin, DeleteView):
    model = DailySale
    template_name = 'sales/dailysale/dailysale_delete.html'
    success_url = reverse_lazy('dailysale-list')

class FoodSaleListView(ListView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_list.html'
    context_object_name = 'foodsales'

class FoodSaleDetailView(DetailView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale.html'
    context_object_name = 'foodsale'

class FoodSaleCreateView(LoginRequiredMixin, CreateView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_create.html'
    fields = ['counter','item','date', 'prepared_quantity', 'leftover_quantity']
    success_url = reverse_lazy('foodsale-list')

class FoodSaleUpdateView(LoginRequiredMixin, UpdateView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_update.html'
    fields = ['counter', 'item','date', 'prepared_quantity', 'leftover_quantity']
    # disable counter field
    def get_form(self, form_class=None):
        form = super(FoodSaleUpdateView, self).get_form(form_class)
        form.fields['counter'].disabled = True
        form.fields['item'].disabled = True
        form.fields['date'].disabled = True
        return form

    success_url = reverse_lazy('foodsale-list')

class FoodSaleDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_delete.html'
    success_url = reverse_lazy('foodsale-list')

# -- forms --

class FoodSaleForm(LoginRequiredMixin ,forms.ModelForm):
    class Meta:
        model = FoodSale
        fields = '__all__'
        # exclude = ('date', 'price', 'counter')

    def __init__(self, *args, **kwargs):
        super(FoodSaleForm, self).__init__(*args, **kwargs)
        self.fields['item'].initial = Item.objects.get(id=self.prefix)
        self.fields['item'].disabled = True

class DailySaleForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = DailySale
        fields = '__all__'

class CounterForm(LoginRequiredMixin, forms.ModelForm):
    # use dropdown to select counter
    class Meta:
        model = Counter
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(CounterForm, self).__init__(*args, **kwargs)
    #     self.fields['counter'].queryset = Counter.objects.all()

@login_required
def dailysale_create(request):
    if request.method == 'POST':
        dailysale_form = DailySaleForm(request.POST, prefix='dailysale')
        counter_form = CounterForm(request.POST, prefix='counter')
        foodsale_forms = [FoodSaleForm(request.POST, prefix=str(item.id)) for item in Item.objects.all()]

        if dailysale_form.is_valid() and counter_form.is_valid() and all([form.is_valid() for form in foodsale_forms]):
            dailysale = dailysale_form.save(commit=False)
            counter = counter_form.cleaned_data['counter']
            foodsales = [form.save(commit=False) for form in foodsale_forms]

            # check if two forms have same item value and add error to that forms
            item_pos = {}
            for i, foodsale in enumerate(foodsales):
                if FoodSale.objects.filter(date=dailysale, item=foodsale.item).exists():
                    foodsale_forms[i].add_error(None, 'Entry for this item already exists')
                if foodsale.item in item_pos:
                    foodsale_forms[i].add_error(None, 'Entry for this item is repeated in the form')
                    foodsale_forms[item_pos[foodsale.item]].add_error(None, 'Entry for this item is repeated in the form')
                else:
                    item_pos[foodsale.item] = i

            if any([form.errors for form in foodsale_forms]):
                return render(request, 'sales/dailysale/dailysale_create.html', {'dailysale_form': dailysale_form, 'foodsale_forms': foodsale_forms, 'counter_form':counter_form, 'date': dailysale.date})
            else:
                dailysale_form.save()
                for form in foodsale_forms:
                    foodsale = form.save(commit=False)
                    foodsale.date = dailysale
                    foodsale.counter = counter
                    foodsale.price = foodsale.item.price
                    foodsale.save()
                return redirect('dailysale', pk=dailysale.pk)
        else:
            return render(request, 'sales/dailysale/dailysale_create.html', {'dailysale_form': dailysale_form, 'foodsale_forms': foodsale_forms, 'counter_form': counter_form})
    else:
        dailysale_form = DailySaleForm(prefix='dailysale', instance=DailySale(date=datetime.date.today()))
        counter_form = CounterForm(prefix='counter')
        foodsale_forms = [FoodSaleForm(prefix=str(item.id), instance=FoodSale(item=item)) for item in Item.objects.all()]
    return render(request, 'sales/dailysale/dailysale_create.html', {'dailysale_form': dailysale_form, 'foodsale_forms': foodsale_forms, 'counter_form': counter_form})

