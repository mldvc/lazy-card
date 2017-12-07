from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _
from app_overview.models import Printer_Ribbon
from .models import Printer_Ribbon_Receive_Record
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


CHOICES = (
    ('RTP', 'RTP Date'),
    ('RD', 'Received Date')
)


class SearchForm(forms.Form):

    dateType = forms.ChoiceField(
        label='Date Type',
        label_suffix=':',
        choices=CHOICES,
        required=True,
    )

    dateFrom = forms.DateField(
        label='From',
        label_suffix=':',
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

    typeSearch = forms.ModelChoiceField(
        label='Ribbon Type',
        label_suffix=':',
        queryset=Printer_Ribbon.objects.all(),
        empty_label='All',
        to_field_name='ribbon_type',
        required=False,
    )

    def clean_dateTo(self):
        dateFrom = self.cleaned_data.get('dateFrom')
        dateTo = self.cleaned_data.get('dateTo')

        if dateFrom > dateTo:
            raise forms.ValidationError(_('Invalid Date.'))

        return dateTo


class StockForm(forms.ModelForm):

    formRibbonType = None
    formRibbonTypeInitial = None
    bolRibbonTypeChanged = False

    objRibbon = None

    formAmount = 0
    formAmountInitial = 0
    bolAmountChanged = False

    class Meta:
        model = Printer_Ribbon_Receive_Record
        fields = [
            "ribbon",
            "rtp_date",
            "received_date",
            "received_amount",
        ]

    def clean_ribbon(self):
        self.formRibbonType = self.cleaned_data.get('ribbon')
        try:
            self.formRibbonTypeInitial = self.initial['ribbon']
        except Exception:
            self.formRibbonTypeInitial = None

        if str(self.formRibbonTypeInitial) != str(self.formRibbonType):
            self.bolRibbonTypeChanged = True

        return self.formRibbonType

    def clean_received_amount(self):
        self.formAmount = self.cleaned_data.get('received_amount')

        if self.formAmount <= 0:
            raise forms.ValidationError(_('Invalid amount.'))

        try:
            self.formAmountInitial = self.initial['received_amount']
        except Exception:
            self.formAmountInitial = 0

        self.objRibbon = Printer_Ribbon.objects.get(ribbon_type=self.formRibbonType)

        if self.bolRibbonTypeChanged:
            self.objRibbon.amount += self.formAmount
            try:
                self.objRibbon.full_clean()
            except Exception:
                raise forms.ValidationError(_('Amount Error.'))
        else:
            if int(self.formAmountInitial) != int(self.formAmount):
                self.bolAmountChanged = True
                prevTotalAmount = int(self.formAmountInitial) - int(self.formAmount)
                if self.formAmount == 0:
                    self.objRibbon.amount -= int(self.formAmountInitial)
                elif int(self.formAmountInitial) > int(self.formAmount):
                    self.objRibbon.amount -= abs(prevTotalAmount)
                else:
                    self.objRibbon.amount += abs(prevTotalAmount)
                try:
                    self.objRibbon.full_clean()
                except Exception:
                    raise forms.ValidationError(_('Amount Error.'))

        return self.formAmount

    # i used a signal pre_delete to do something before deleting
    @receiver(pre_delete, sender=Printer_Ribbon_Receive_Record)
    def _IDPrintRecord_delete(sender, instance, **kwargs):
        totalRibbonToReturn = instance.received_amount
        prevRibbonType = Printer_Ribbon.objects.get(ribbon_type=instance.ribbon)
        testAmount = prevRibbonType.amount - totalRibbonToReturn
        if testAmount < 0:
            prevRibbonType.amount = 0
        else:
            prevRibbonType.amount -= totalRibbonToReturn
        try:
            prevRibbonType.full_clean()
            prevRibbonType.save()
        except Exception:
            raise forms.ValidationError(_('Amount Error.'))

    def save(self, commit=True):
        instance = super(StockForm, self).save(commit=False)

        if instance._state.adding is True:
            self.objRibbon.save()
        else:
            if self.has_changed():
                if self.bolRibbonTypeChanged:
                    prevTotalAmount = int(self.formAmountInitial)
                    prevRibbonType = Printer_Ribbon.objects.get(ribbon_type=str(self.formRibbonTypeInitial))
                    prevRibbonType.amount -= prevTotalAmount
                    prevRibbonType.full_clean()
                    prevRibbonType.save()
                    self.objRibbon.save()

                if self.bolAmountChanged:
                    if not self.bolRibbonTypeChanged:
                        self.objRibbon.save()

        if commit:
            instance.save()
        return instance
