from django.contrib import admin
from .models import Printer_Ribbon_Receive_Record
from .forms import StockForm


class Printer_Ribbon_Receive_Record_Admin(admin.ModelAdmin):
    list_display = ['ribbon', 'received_date', 'received_amount']

    form = StockForm


admin.site.register(Printer_Ribbon_Receive_Record, Printer_Ribbon_Receive_Record_Admin)
