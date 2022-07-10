from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ListOfCountries
from .models import Accommodation


def main(request):
    return render(request, 'mainapp/index.html')


def accommodations(request):
    title = 'размещения'

    list_of_accommodations = Accommodation.objects.filter(is_active=True)

    content = {
        'title': title,
        'list_of_accommodations': list_of_accommodations,
    }

    return render(request, 'mainapp/accommodations.html', content)


def accommodation(request, pk):
    title = 'размещение'

    content = {
        'title': title,
        'accommodation': get_object_or_404(Accommodation, pk=pk),
    }

    return render(request, 'mainapp/accommodations_details.html', content)
