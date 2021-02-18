from django.http import Http404
from django.shortcuts import render
from data_processing_app.models import toggl_clients
import data_processing_app.models as models
from django.db.models.functions import ExtractWeek
from django.db.models import Sum

# def example(request):
#     week_sum = models.time_entries.objects.filter(project__client__name="DI") \
#         .annotate(week=ExtractWeek('start')).values('week') \
#         .annotate(week_total=Sum('duration') / 3600) \
#         .order_by('week')
#
#     return render(request, 'example.html', {'week_sum': week_sum})

def example(request):
    test_string = "Hello World!"
    time_entries = models.time_entries.objects.all()
    context = {'test_string': test_string,
               'time_entries': time_entries}

    return render(request, 'example2.html', context)

# QuerSet = models.time_entries.objects.filter(project__client__name="DI") \
#         .annotate(week=ExtractWeek('start')).values('week') \
#         .annotate(week_total=Sum('duration') / 3600) \
#         .order_by('week')