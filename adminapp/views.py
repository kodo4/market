from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from mainapp.models import Accommodation, ListOfCountries
from authapp.forms import TravelUser, TravelUserRegisterForm
from adminapp.forms import TravelUserAdminEditForm, AccommodationEditForm


# Админка - список пользователей
class TravelUsersListView(ListView):
    model = TravelUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# админка - создание пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = TravelUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = TravelUserRegisterForm

    content = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', content)


# админка - редактирование пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(TravelUser, pk=pk)

    if request.method == 'POST':
        edit_form = TravelUserAdminEditForm(request.POST,
                                            request.FILES,
                                            instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = TravelUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', content)


# админка - удаление пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(TravelUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', content)


# админка - список старн
@user_passes_test(lambda u: u.is_superuser)
def countries(request):
    title = 'админка/страны'

    countries_list = ListOfCountries.objects.all()

    content = {
        'title': title,
        'objects': countries_list,
    }

    return render(request, 'adminapp/countries.html', content)


# админка - создание страны
class CountryCreateView(CreateView):
    model = ListOfCountries
    template_name = 'adminapp/country_update.html'
    success_url = reverse_lazy('admin:countries')
    fields = '__all__'


# админка - редактирование страны
class CountryUpdateView(UpdateView):
    model = ListOfCountries
    template_name = 'adminapp/country_update.html'
    success_url = reverse_lazy('admin:countries')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'страны/редактирование'

        return context


# админка - удаление страны
class CountryDeleteView(DeleteView):
    model = ListOfCountries
    template_name = 'adminapp/country_delete.html'
    success_url = reverse_lazy('admin:countries')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
