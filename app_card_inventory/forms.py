from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _
from app_overview.models import ID_Card
from .models import ID_Card_Receive_Record
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
        label='Card Type',
        label_suffix=':',
        queryset=ID_Card.objects.all(),
        empty_label='All',
        to_field_name='card_type',
        required=False,
    )

    def clean_dateTo(self):
        dateFrom = self.cleaned_data.get('dateFrom')
        dateTo = self.cleaned_data.get('dateTo')

        if dateFrom > dateTo:
            raise forms.ValidationError(_('Invalid Date.'))

        return dateTo


class StockForm(forms.ModelForm):

    formCardType = None
    formCardTypeInitial = None
    bolCardTypeChanged = False

    objCard = None

    formAmount = 0
    formAmountInitial = 0
    bolAmountChanged = False

    class Meta:
        model = ID_Card_Receive_Record
        fields = [
            "card",
            "rtp_date",
            "received_date",
            "received_box_amount",
            "received_amount",
        ]

    def clean_card(self):
        self.formCardType = self.cleaned_data.get('card')
        try:
            self.formCardTypeInitial = self.initial['card']
        except Exception:
            self.formCardTypeInitial = None

        if str(self.formCardTypeInitial) != str(self.formCardType):
            self.bolCardTypeChanged = True

        return self.formCardType

    def clean_received_box_amount(self):
        formBoxAmount = self.cleaned_data.get('received_box_amount')
        if formBoxAmount == 0:
            raise forms.ValidationError(_('Invalid amount.'))
        return formBoxAmount

    def clean_received_amount(self):
        self.formAmount = self.cleaned_data.get('received_amount')

        if self.formAmount <= 0:
            raise forms.ValidationError(_('Invalid amount.'))

        try:
            self.formAmountInitial = self.initial['received_amount']
        except Exception:
            self.formAmountInitial = 0

        self.objCard = ID_Card.objects.get(card_type=self.formCardType)

        if self.bolCardTypeChanged:
            self.objCard.amount += self.formAmount
            try:
                self.objCard.full_clean()
            except Exception:
                raise forms.ValidationError(_('Amount Error.'))
        else:
            if int(self.formAmountInitial) != int(self.formAmount):
                self.bolAmountChanged = True
                prevTotalAmount = int(self.formAmountInitial) - int(self.formAmount)
                if self.formAmount == 0:
                    self.objCard.amount -= int(self.formAmountInitial)
                elif int(self.formAmountInitial) > int(self.formAmount):
                    self.objCard.amount -= abs(prevTotalAmount)
                else:
                    self.objCard.amount += abs(prevTotalAmount)
                try:
                    self.objCard.full_clean()
                except Exception:
                    raise forms.ValidationError(_('Amount Error.'))

        return self.formAmount

    # i used a signal pre_delete to do something before deleting
    @receiver(pre_delete, sender=ID_Card_Receive_Record)
    def _IDPrintRecord_delete(sender, instance, **kwargs):
        totalCardToReturn = instance.received_amount
        prevCardType = ID_Card.objects.get(card_type=instance.card)
        testAmount = prevCardType.amount - totalCardToReturn
        if testAmount < 0:
            prevCardType.amount = 0
        else:
            prevCardType.amount -= totalCardToReturn
        try:
            prevCardType.full_clean()
            prevCardType.save()
        except Exception:
            raise forms.ValidationError(_('Amount Error.'))

    def save(self, commit=True):
        instance = super(StockForm, self).save(commit=False)

        if instance._state.adding is True:
            self.objCard.save()
        else:
            if self.has_changed():
                if self.bolCardTypeChanged:
                    prevTotalAmount = int(self.formAmountInitial)
                    prevCardType = ID_Card.objects.get(card_type=str(self.formCardTypeInitial))
                    prevCardType.amount -= prevTotalAmount# return the deducted card in previous card type
                    prevCardType.full_clean()
                    prevCardType.save()# save
                    self.objCard.save()# save

                if self.bolAmountChanged:
                    if not self.bolCardTypeChanged:
                        self.objCard.save()# save

        if commit:
            instance.save()
        return instance
