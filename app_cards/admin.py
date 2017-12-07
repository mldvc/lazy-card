from django.contrib import admin
from .models import IDPrintRecord, CardUsageHistory
from .forms import PrintHistoryForm, CardUsageHistoryForm


class IDPrintRecordAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'id_type', 'print_date']
    form = PrintHistoryForm


class CardUsageHistoryAdmin(admin.ModelAdmin):
    list_display = ['card', 'use_date', 'amount']
    form = CardUsageHistoryForm


admin.site.register(IDPrintRecord, IDPrintRecordAdmin)
admin.site.register(CardUsageHistory, CardUsageHistoryAdmin)
