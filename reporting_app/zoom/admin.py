from django.contrib import admin

from .forms import ZoomForm
from .models import Zoom


class ZoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', )
    form = ZoomForm


admin.site.register(Zoom, ZoomAdmin)
