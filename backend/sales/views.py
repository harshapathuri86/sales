import datetime
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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

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
    fields = ['item','date', 'prepared_quantity', 'leftover_quantity']
    success_url = reverse_lazy('foodsale-list')

class FoodSaleUpdateView(LoginRequiredMixin, UpdateView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_update.html'
    fields = ['item','date', 'prepared_quantity', 'leftover_quantity']
    success_url = reverse_lazy('foodsale-list')

class FoodSaleDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodSale
    template_name = 'sales/foodsale/foodsale_delete.html'
    success_url = reverse_lazy('foodsale-list')

class DailySaleForm(LoginRequiredMixin, ModelForm):
    class Meta:
        model = DailySale
        fields = '__all__'

class FoodSaleForm(LoginRequiredMixin ,ModelForm):
    class Meta:
        model = FoodSale
        fields = '__all__'
        exclude = ('date', 'price')

# login required
@login_required
def daily_add(request):
    # create a form that takes dailysale form, multiple foodsale forms each for each item
    # add a food form each for each item
    # and a submit button
    if request.method == 'POST':
        dailysale_form = DailySaleForm(request.POST, prefix='dailysale')
        foodsale_forms = [FoodSaleForm(request.POST, prefix=str(item.id)) for item in Item.objects.all()]
        if dailysale_form.is_valid() and all([form.is_valid() for form in foodsale_forms]):
            dailysale = dailysale_form.save(commit=False)
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
                return render(request, 'sales/dailysale/dailysale_create.html', {'dailysale_form': dailysale_form, 'foodsale_forms': foodsale_forms, 'date': dailysale.date})
            else:
                dailysale_form.save()
                for form in foodsale_forms:
                    foodsale = form.save(commit=False)
                    foodsale.date = dailysale
                    foodsale.price = foodsale.item.price
                    foodsale.save()
                return redirect('dailysale', pk=dailysale.pk)
        else:
            return render(request, 'sales/dailysale/dailysale_create.html', {'dailysale_form': dailysale_form, 'foodsale_forms': foodsale_forms})
    else:
        dailysale_form = DailySaleForm(prefix='dailysale', instance=DailySale(date=datetime.date.today()))
        foodsale_forms = [FoodSaleForm(prefix=str(item.id), instance=FoodSale(item=item)) for item in Item.objects.all()]
    return render(request, 'sales/dailysale/dailysale_create.html', {'dailysale_form': dailysale_form, 'foodsale_forms': foodsale_forms})

@login_required
def daily_update(request, pk=None):
    dailysale = DailySale.objects.get(pk=pk)
    if request.method == 'POST':
        foodsale_forms = [FoodSaleForm(request.POST, prefix=str(item.id)) for item in Item.objects.all()]

        if all([form.is_valid() for form in foodsale_forms]):
            foodsales = [form.save(commit=False) for form in foodsale_forms]
            # check if two forms have same item value and add error to that forms
            item_pos = {}
            for i, foodsale in enumerate(foodsales):
                if foodsale.item in item_pos:
                    foodsale_forms[i].add_error(None, 'Entry for this item is repeated in the form')
                else:
                    item_pos[foodsale.item] = i
            if any([form.errors for form in foodsale_forms]):
                return render(request, 'sales/dailysale/dailysale_update.html', {'foodsale_forms': foodsale_forms, 'date': dailysale.date})
            else:
                for form in foodsale_forms:
                    # update record
                    foodsale = form.save(commit=False)
                    foodsale.date = dailysale
                    FoodSale.objects.filter(date=dailysale, item=foodsale.item).update(**form.cleaned_data)

                return redirect('dailysale', pk=dailysale.pk)
        else:
            return render(request, 'sales/dailysale/dailysale_update.html', {'foodsale_forms': foodsale_forms, 'date': dailysale.date})
    else:
        # if not all items have food sale, put 0 s and show form
        # if all items have food sale, show form with values
        foodsale_forms = []
        for item in Item.objects.all():
            if FoodSale.objects.filter(date=dailysale, item=item).exists():
                foodsale_forms.append(FoodSaleForm(prefix=str(item.id), instance=FoodSale.objects.get(date=dailysale, item=item)))
            else:
                foodsale_forms.append(FoodSaleForm(prefix=str(item.id), instance=FoodSale(item=item)))
    return render(request, 'sales/dailysale/dailysale_update.html', {'date': dailysale.date, 'foodsale_forms': foodsale_forms})
