from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from .models import Order, OrderItem
from .forms import OrderItemForm


# список заказов
class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# Создание заказа
class OrderItemCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1,
                                             fields='__all__')

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order,
                                                     OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items),
                                                     fields='__all__')
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['accommodation'] = \
                        basket_items[num].accommodation
                    form.initial['nights'] = basket_items[num].nights
                    form.initial['price'] = \
                        basket_items[num].accommodation.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super(OrderItemCreate, self).form_valid(form)


# Редактирование заказа
class OrderItemUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1,
                                             fields='__all__')

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST,
                                              instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.accommodation.price
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super(OrderItemUpdate, self).form_valid(form)


# Карточка заказ
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


# удаление товара из заказа
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


# перевод статуса заказа
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))
