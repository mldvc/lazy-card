from django.contrib import admin
from .models import ID_Card, Printer_Ribbon, Active_Stocks, UserProfile


class IDCardAdmin(admin.ModelAdmin):
    list_display = ['card_type', 'amount']


class PrinterRibbonAdmin(admin.ModelAdmin):
    list_display = ['ribbon_type', 'amount']


class ActiveStockAdmin(admin.ModelAdmin):
    list_display = ['stock_name', 'amount']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'printer', 'active_card', 'all_types']


admin.site.register(ID_Card, IDCardAdmin)
admin.site.register(Printer_Ribbon, PrinterRibbonAdmin)
admin.site.register(Active_Stocks, ActiveStockAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
