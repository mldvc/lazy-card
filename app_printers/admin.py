from django.contrib import admin
from .models import Printers


# Register your models here.
class PrintersAdmin(admin.ModelAdmin):
    list_display = ['printer_name', 'total_printed', 'status']


admin.site.register(Printers, PrintersAdmin)
