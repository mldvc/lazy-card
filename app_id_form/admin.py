from django.contrib import admin
from .models import ID_Form, FormFields
from .forms import IDForm, FieldsForm


class ID_FormAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_display = ['full_name', 'id_type']

    form = IDForm


class FormFieldsAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = FieldsForm


admin.site.register(ID_Form, ID_FormAdmin)
admin.site.register(FormFields, FormFieldsAdmin)
