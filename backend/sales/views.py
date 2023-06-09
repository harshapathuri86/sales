import datetime
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Count, Aggregate
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from .models import *
from .forms import *

@login_required
def select_counter(request):
    if request.method == 'POST':
        form = CounterSelectForm(request.POST)
        if form.is_valid():
            counter = form.cleaned_data['counter']
            date = form.cleaned_data['date']
            sale_type = form.cleaned_data['sale_type']
            # check if foodsale with this counter on this date exists
            if FoodSale.objects.filter(counter=counter, date=date, sale_type=sale_type).exists():
                form.add_error('counter', 'FoodSale with this counter on this date for this time already exists')
                return render(request, 'sales/counter/counter_select.html', {'form': form})
            else:
                return redirect('dailysale-add', counter_id=counter.id, date=date, sale_type=sale_type)
    return render(request, 'sales/counter/counter_select.html', {'form': CounterSelectForm})

@login_required
def add_sale(request, counter_id, date, sale_type):
    counter = Counter.objects.get(id=counter_id)
    items = Item.objects.all()
    if request.method == 'POST':
        forms = []
        forms = [ FoodSaleForm(request.POST, prefix=item.id) for item in items ]

        if all([ form.is_valid() for form in forms ]):
            for form in forms:
                form.save()
            return redirect('dailysale-list')
        else:
            return render(request, 'sales/dailysale/dailysale_add.html', {'forms': forms, 'counter': counter, 'date': date, 'sale_type': sale_type})

    if request.method == 'GET':
        forms = []
        for item in items:
            form = FoodSaleForm(initial={'item': item, 'counter': counter, 'date': date, 'sale_type': sale_type}, prefix=item.id)
            forms.append(form)
        return render(request, 'sales/dailysale/dailysale_add.html', {'forms': forms, 'counter': counter, 'date': date, 'sale_type': sale_type})

# write a view to compute daily sale and show it
def dailysale_list(request):

    dailysales = FoodSale.objects.values('date', 'counter', 'counter__name', 'sale_type').annotate(total_sale=Sum((F('outgoing')-F('incoming'))*F('price'))).order_by('-date')

    context = {'dailysales':dailysales}
    return render(request, 'sales/dailysale/dailysale_list.html', context)

def dailysale_view(request, counter_id, date, sale_type):

    # filter sale based on date and then group by counter and calculate sale
    # dailysale = FoodSale.objects.filter(date=date, counter = counter_id, sale_type = sale_type).values('counter__name').annotate(total_sale=Sum((F('outgoing')-F('incoming'))*F('price'))).order_by('-total_sale')

    counter_name = Counter.objects.get(id=counter_id).name

    foodsales = FoodSale.objects.filter(date=date, counter = counter_id, sale_type = sale_type).order_by('item')

    total_sale = foodsales.aggregate(total_sale=Sum((F('outgoing')-F('incoming'))*F('price')))['total_sale']

    context = {'counter':counter_name, 'foodsales':foodsales, 'total_sale': total_sale, 'date':date, 'sale_type': sale_type}
    return render(request, 'sales/dailysale/dailysale.html', context)


# generic views

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
    fields = ['item', 'date', 'counter', 'outgoing', 'incoming']
    success_url = reverse_lazy('foodsale-list')

class FoodSaleUpdateView(LoginRequiredMixin, UpdateView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_update.html'
    fields = ['item', 'date', 'counter', 'outgoing', 'incoming']
    success_url = reverse_lazy('foodsale-list')

class FoodSaleDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_delete.html'
    success_url = reverse_lazy('foodsale-list')

 
