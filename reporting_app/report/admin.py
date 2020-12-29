from django.contrib import admin

from .forms import ReportForm
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'type',)
    form = ReportForm
    list_filter = ('type',)


admin.site.register(Report, ReportAdmin)
