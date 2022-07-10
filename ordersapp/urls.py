from django.urls import path

from .views import OrderList, OrderItemCreate, OrderItemUpdate, OrderRead, \
    OrderDelete, order_forming_complete

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderList.as_view(), name='orders_list'),
    path('create/', OrderItemCreate.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderItemUpdate.as_view(), name='order_update'),
    path('read/<int:pk>/', OrderRead.as_view(), name='order_read'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='order_delete'),
    path('forming/comlete/<int:pk>/', order_forming_complete,
         name='order_forming_complete'),

]
