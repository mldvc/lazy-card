from django.contrib import admin
from .models import ID_Card_Receive_Record
from .forms import StockForm


class ID_Card_Receive_Record_Admin(admin.ModelAdmin):
    list_display = ['card', 'received_date', 'received_amount']
    form = StockForm


admin.site.register(ID_Card_Receive_Record, ID_Card_Receive_Record_Admin)
