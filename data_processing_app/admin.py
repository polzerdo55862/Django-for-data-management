from django.contrib import admin
from data_processing_app.models import time_entries,vacation_days,toggl_conf,toggl_workspaces,toggl_projects,toggl_clients
from django.db.models.functions import ExtractWeek
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from django.http import JsonResponse

# @admin.register(toggl_conf)
# class ConfAdmin(admin.ModelAdmin):
#     list_display = ('variable', 'value')
#     fields = ('variable', 'value')

@admin.register(toggl_clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('cid', 'name')
#
# @admin.register(toggl_projects)
# class ConfAdmin(admin.ModelAdmin):
#     list_display = ('pid', 'project_name')
#
# @admin.register(time_entries)
# class EntriesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'project_name', 'client_name', 'duration', 'start',
#                     'start_week')
#     def project_name(self, obj):
#         #import pdb;pdb.set_trace()
#         return obj.project.project_name
#
#     def client_name(self, obj):
#         return obj.project.client.name
#
#     def start_week(self, obj):
#         week = obj.start.isocalendar()[1]
#         return week
#     # client_name.short_description = 'Projekt Name'
#
#     def changelist_view(self, request, extra_context=None):
#         # Aggregate new subscribers per day
#         chart_data = (
#             time_entries.objects.filter(project__client__name="DI") \
#                 .annotate(x=ExtractWeek('start')).values('x') \
#                 .annotate(y=Sum('duration') / 3600) \
#                 .order_by('x')
#         )
#
#         xaxis = []
#         yaxis = []
#
#         for line in chart_data:
#             #import pdb;pdb.set_trace()
#             xaxis.append(str(line["x"]))
#             yaxis.append(line["y"])
#
#         # Serialize and attach the chart data to the template context
#         #as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
#         extra_context = {"x": xaxis, "y": yaxis}
#
#         #import pdb;pdb.set_trace()
#         # Call the superclass changelist_view to render the page
#         return super().changelist_view(request, extra_context=extra_context)

# Register your models here.
#admin.site.register(toggl_conf, ConfAdmin)
# admin.site.register(toggl_clients)
# admin.site.register(toggl_projects)
#admin.site.register(toggl_conf, ConfAdmin)
#admin.site.register(time_entries, EntriesAdmin)
