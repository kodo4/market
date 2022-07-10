from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/read/', adminapp.TravelUsersListView.as_view(), name='users'),
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('countries/read/', adminapp.countries, name='countries'),
    path('countries/create/', adminapp.CountryCreateView.as_view(),
         name='country_create'),
    path('countries/update/<int:pk>/', adminapp.CountryUpdateView.as_view(),
         name='country_update'),
    path('countries/delete/<int:pk>/', adminapp.CountryDeleteView.as_view(),
         name='country_delete'),
]
