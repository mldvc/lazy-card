from django.contrib import admin
from .models import RibbonUsageRecord
from .forms import CRUDRibbonUsageForm


class RibbonUsageRecordAdmin(admin.ModelAdmin):
    search_fields = ['ribbon_status']
    list_display = [
        'ribbon_number',
        'ribbon_type',
        'ribbon_printer',
        'ribbon_status',
        'ribbon_total_printed',
        'ribbon_use_date',
    ]

    form = CRUDRibbonUsageForm


admin.site.register(RibbonUsageRecord, RibbonUsageRecordAdmin)
