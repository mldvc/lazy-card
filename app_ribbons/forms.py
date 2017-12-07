from django import forms
from .models import RibbonUsageRecord
from app_overview.models import Printer_Ribbon
import datetime
from django.utils.translation import ugettext_lazy as _


class UpdateRibbonUsageForm(forms.ModelForm):
    class Meta:
        model = RibbonUsageRecord
        fields = [
            "ribbon_number",
            "ribbon_use_date",
            "ribbon_status",
            "ribbon_total_printed",
        ]


class CRUDRibbonUsageForm(forms.ModelForm):
    # prevRibbonStatus = forms.BooleanField(
    #     label='Empty Previous Ribbon',
    #     label_suffix=':',
    #     initial=True,
    #     required=False,
    # )

    class Meta:
        model = RibbonUsageRecord
        fields = [
            "ribbon_number",
            "ribbon_type",
            "ribbon_use_date",
            "ribbon_printer",
            "ribbon_status",
            "ribbon_total_printed",
            # "prevRibbonStatus",
        ]

    objRibbon = None

    formRibbonType = None
    formRibbonTypeInitial = None
    bolRibbonTypeChanged = False

    def clean_ribbon_number(self):
        self.formRibbonNumber = self.cleaned_data.get('ribbon_number')
        if self.formRibbonNumber <= 0:
            raise forms.ValidationError(_('Invalid ribbon number.'))

        return self.formRibbonNumber

    def clean_ribbon_type(self):
        self.formRibbonType = self.cleaned_data.get('ribbon_type')
        try:
            self.formRibbonTypeInitial = self.initial['ribbon_type'].ribbon_type
        except Exception:
            try:
                self.formRibbonTypeInitial = self.initial['ribbon_type']
            except Exception:
                self.formRibbonTypeInitial = None

        self.objRibbon = Printer_Ribbon.objects.get(ribbon_type=self.formRibbonType)
        if str(self.formRibbonType) != str(self.formRibbonTypeInitial):
            self.bolRibbonTypeChanged = True
        self.objRibbon.amount -= 1
        try:
            self.objRibbon.full_clean()
        except Exception:
            raise forms.ValidationError(_('{} Ribbon stock is empty.'.format(
                self.objRibbon.ribbon_type)))

        return self.formRibbonType

    def clean_ribbon_total_printed(self):
        self.formTotalPrinted = self.cleaned_data.get('ribbon_total_printed')
        if self.formTotalPrinted < 0:
            raise forms.ValidationError(_('Invalid total printed.'))

        return self.formTotalPrinted

    def save(self, commit=True):
        instance = super(CRUDRibbonUsageForm, self).save(commit=False)

        if instance._state.adding is True:
            self.objRibbon.save()
        else:
            if self.has_changed():
                if self.bolRibbonTypeChanged:
                    prevRibbonType = Printer_Ribbon.objects.get(ribbon_type=str(self.formRibbonTypeInitial))
                    prevRibbonType.amount += 1
                    self.objRibbon.save()
                    try:
                        prevRibbonType.full_clean()
                        prevRibbonType.save()
                    except Exception:
                        raise forms.ValidationError(_('Returning stock error.'))

        if commit:
            instance.save()
        return instance


class RibbonUsageForm(forms.Form):

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

    ribbonTypeSearch = forms.ModelChoiceField(
        label='Ribbon Type',
        label_suffix=':',
        queryset=Printer_Ribbon.objects.all(),
        empty_label='All',
        to_field_name='ribbon_type',
        required=False,
    )

    ribbonNumberSearch = forms.IntegerField(
        label='Ribbon No',
        label_suffix='.',
        required=False,
    )

    statusSearch = forms.ChoiceField(
        required=False,
        label='Status',
        label_suffix=':',
        choices=(('ALL', 'All'),) + RibbonUsageRecord.STATUS
    )

    def clean_dateTo(self):
        dateFrom = self.cleaned_data.get('dateFrom')
        dateTo = self.cleaned_data.get('dateTo')

        if dateFrom > dateTo:
            raise forms.ValidationError(_('Invalid Date.'))

        return dateTo
