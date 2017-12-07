from django import forms
import datetime
from app_reference.models import IDTypes
from django.utils.translation import ugettext_lazy as _


class PrintForm(forms.Form):
    dateFrom = forms.DateField(
        label='From',
        label_suffix=':',
        initial=datetime.date.today,
        required=True,
        input_formats=[
            '%Y-%m-%d',      # '2006-10-25'
            '%m/%d/%Y',      # '10/25/2006'
            '%m/%d/%y']      # '10/25/06
    )

    dateTo = forms.DateField(
        label='To',
        label_suffix=':',
        initial=datetime.date.today,
        required=True,
        input_formats=[
            '%Y-%m-%d',      # '2006-10-25'
            '%m/%d/%Y',      # '10/25/2006'
            '%m/%d/%y']      # '10/25/06
    )

    idtypeSearch = forms.ModelChoiceField(
        label='ID Type',
        label_suffix=':',
        queryset=IDTypes.objects.all(),
        empty_label='All',
        to_field_name='type',
        required=False,
    )

    def clean_dateTo(self):
        dateFrom = self.cleaned_data.get('dateFrom')
        dateTo = self.cleaned_data.get('dateTo')

        if dateFrom > dateTo:
            raise forms.ValidationError(_('Invalid Date.'))

        return dateTo
