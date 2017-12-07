from django import forms
from .models import IDPrintRecord, CardUsageHistory
from app_overview.models import ID_Card
from app_ribbons.models import RibbonUsageRecord
from app_printers.models import Printers
from django.utils.translation import ugettext_lazy as _
from app_overview.models import Active_Stocks
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from app_reference.models import IDTypes
import datetime


class CardUsageHistoryForm(forms.ModelForm):
    class Meta:
        model = CardUsageHistory
        fields = [
            "card",
            "use_date",
            "amount",
        ]

    objCardType = None
    objActiveCard = None
    bolCardChanged = False
    frmCardInitial = None
    frmCard = None

    frmAmount = 0
    frmAmountInitial = 0
    bolAmountChanged = False

    def clean_card(self):
        self.frmCard = self.cleaned_data.get('card')
        try:
            self.frmCardInitial = self.initial['card']
        except Exception:
            self.frmCardInitial = None
        if self.frmCard.id != self.frmCardInitial:
            self.bolCardChanged = True
        return self.frmCard

    def clean_amount(self):
        self.frmAmount = self.cleaned_data.get('amount')
        if self.frmAmount <= 0:
            raise forms.ValidationError(_('Invalid amount.'))
        try:
            self.frmAmountInitial = self.initial['amount']
        except Exception:
            self.frmAmountInitial = None

        self.objActiveCard = Active_Stocks.objects.get(id=self.frmCard.id)
        self.objCardType = ID_Card.objects.get(id=self.frmCard.card_type.id)

        if self.bolCardChanged:
            self.objActiveCard.amount += self.frmAmount
            try:
                self.objActiveCard.full_clean()
            except Exception:
                raise forms.ValidationError(_('Adding active card stock error.'))

            self.objCardType.amount -= self.frmAmount
            try:
                self.objCardType.full_clean()
            except Exception:
                raise forms.ValidationError(_('Card stock shortage.'))
        else:
            if int(self.frmAmount) != int(self.frmAmountInitial):
                self.bolAmountChanged = True
                prevTotalAmount = int(self.frmAmountInitial) - int(self.frmAmount)
                if self.frmAmount == 0:
                    self.objActiveCard.amount -= int(self.frmAmountInitial)
                    self.objCardType.amount += int(self.frmAmountInitial)
                elif int(self.frmAmountInitial) > int(self.frmAmount):
                    self.objActiveCard.amount -= abs(prevTotalAmount)
                    self.objCardType.amount += abs(prevTotalAmount)
                else:
                    self.objActiveCard.amount += abs(prevTotalAmount)
                    self.objCardType.amount -= abs(prevTotalAmount)
                try:
                    self.objActiveCard.full_clean()
                except Exception:
                    raise forms.ValidationError(_('Updating active card stock error.'))
                try:
                    self.objCardType.full_clean()
                except Exception:
                    raise forms.ValidationError(_('Card stock shortage.'))
        return self.frmAmount

    # i used a signal pre_delete to do something before deleting
    @receiver(pre_delete, sender=CardUsageHistory)
    def _IDPrintRecord_delete(sender, instance, **kwargs):
        totalCardsToReturn = instance.amount

        cardType = ID_Card.objects.get(id=instance.card.card_type.id)
        cardType.amount += totalCardsToReturn
        try:
            cardType.full_clean()
            cardType.save()
        except Exception:
            raise forms.ValidationError(_('Card type error.'))

        activeCard = Active_Stocks.objects.get(id=instance.card.id)
        testAmount = activeCard.amount - totalCardsToReturn
        if testAmount < 0:
            activeCard.amount = 0
        else:
            activeCard.amount -= totalCardsToReturn
        try:
            activeCard.full_clean()
            activeCard.save()
        except Exception:
            raise forms.ValidationError(_('Active card error.'))

    def save(self, commit=True):
        instance = super(CardUsageHistoryForm, self).save(commit=False)

        if instance._state.adding is True:
            self.objActiveCard.save()
            self.objCardType.save()
        else:
            if self.has_changed():
                orig_obj = self._meta.model.objects.get(pk=instance.pk)
                if self.bolCardChanged:
                    prevTotalAmount = int(self.frmAmountInitial)
                    print(self.frmCardInitial)

                    prevCardType = ID_Card.objects.get(id=orig_obj.card.card_type.id)
                    prevCardType.amount += prevTotalAmount
                    prevCardType.full_clean()
                    prevCardType.save()
                    self.objCardType.save()

                    prevActiveCard = Active_Stocks.objects.get(id=orig_obj.card.id)
                    testAmount = prevActiveCard.amount - prevTotalAmount
                    if testAmount < 0:
                        prevActiveCard.amount = 0
                    else:
                        prevActiveCard.amount -= prevTotalAmount
                    prevActiveCard.full_clean()
                    prevActiveCard.save()
                    self.objActiveCard.save()

                if self.bolAmountChanged:
                    if not self.bolCardChanged:
                        self.objActiveCard.save()
                        self.objCardType.save()

        if commit:
            instance.save()
        return instance


class PrintHistoryForm(forms.ModelForm):
    objUsedRibbon = None
    objActiveRibbon = None

    objActivePrinters = None
    objUsedPrinter = None
    bolPrinterChanged = False
    formPrinterInitial = 0

    objUsedCard = None
    bolCardChanged = False
    formCardInitial = None

    bolBadPrintChanged = False
    formBadPrintInitial = None
    formBadPrint = 0

    DICT_MESSAGE = {}
    DICT_FIELDS = {}
    LIST_FIELDS = []

    class Meta:
        model = IDPrintRecord
        fields = [
            "id_number",
            "name",
            "id_type",
            "bad_print",
            "print_date",
            "card",
            "id_status",
            "printer",
        ]

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop('request')
        except Exception:
            self.request = None

        super(PrintHistoryForm, self).__init__(*args, **kwargs)
        self.objActivePrinters = Printers.objects.filter(status="A")
        objActiveStocks = Active_Stocks.objects.all()
        objIDTypes = IDTypes.objects.all()
        if self.request is not None:
            try:
                bolAllIDTypes = self.request.user.userprofile.all_types
            except AttributeError:
                bolAllIDTypes = True

            try:
                activeCardID = self.request.user.userprofile.active_card.id
            except AttributeError:
                activeCardID = None

            try:
                printerID = self.request.user.userprofile.printer.id
            except AttributeError:
                printerID = None

            try:
                officeID = self.request.user.userprofile.printer.office.id
            except AttributeError:
                officeID = None

            if activeCardID is not None:
                self.fields['card'].queryset = objActiveStocks.filter(
                    id=activeCardID
                )

            if printerID is not None:
                self.fields['printer'].queryset = self.objActivePrinters.filter(
                    id=printerID
                )

            if bolAllIDTypes is False:
                if officeID is not None:
                    self.fields['id_type'].queryset = objIDTypes.filter(
                        office__id=officeID
                    )

    def clean_id_number(self):
        formIDNumber = self.cleaned_data.get('id_number')
        try:
            formIDNumberInitial = self.initial['id_number']
        except Exception:
            formIDNumberInitial = 0

        if str(formIDNumberInitial) != str(formIDNumber):
            self.LIST_FIELDS.append('ID number')

        return formIDNumber

    def clean_name(self):
        formName = self.cleaned_data['name']
        try:
            formNameInitial = self.initial['name']
        except Exception:
            formNameInitial = None

        if str(formNameInitial) != str(formName):
            self.LIST_FIELDS.append('name')

        return formName.upper()

    def clean_bad_print(self):
        self.formBadPrint = self.cleaned_data.get('bad_print')

        if self.formBadPrint < 0:
            raise forms.ValidationError(_('Invalid amount of bad print'))
        try:
            self.formBadPrintInitial = self.initial['bad_print']
        except Exception:
            self.formBadPrintInitial = 0

        if int(self.formBadPrintInitial) != int(self.formBadPrint):
            self.bolBadPrintChanged = True

        return self.formBadPrint

    def clean_id_type(self):
        formIDType = self.cleaned_data.get('id_type')
        try:
            formIDTypeInitial = self.initial['id_type']
        except Exception:
            formIDTypeInitial = None
        if str(formIDTypeInitial) != str(formIDType):
            self.LIST_FIELDS.append('ID type')

        return formIDType

    def clean_card(self):
        formCardType = self.cleaned_data.get('card')
        try:
            self.formCardInitial = self.initial['card']
        except Exception:
            self.formCardInitial = None

        self.objUsedCard = Active_Stocks.objects.get(id=formCardType.id)

        if self.formCardInitial != formCardType.id:
            self.bolCardChanged = True
            totalUsedCard = 1 + self.formBadPrint
            self.objUsedCard.amount -= totalUsedCard
            try:
                self.objUsedCard.full_clean()
            except Exception:
                raise forms.ValidationError(_('{} Stock Shortage.'.format(formCardType.stock_name)))
        else:
            if self.bolBadPrintChanged:
                totalCardUsed = int(self.formBadPrintInitial) - int(self.formBadPrint)
                if self.formBadPrint == 0:
                    self.objUsedCard.amount += int(self.formBadPrintInitial)
                elif int(self.formBadPrintInitial) > int(self.formBadPrint):
                    self.objUsedCard.amount += abs(totalCardUsed)
                else:
                    self.objUsedCard.amount -= abs(totalCardUsed)
                try:
                    self.objUsedCard.full_clean()
                except Exception:
                    raise forms.ValidationError(_('{} Stock Shortage.'.format(formCardType.stock_name)))

        return formCardType

    def clean_print_date(self):
        formPrintDate = self.cleaned_data.get('print_date')
        try:
            formPrintDateInitital = self.initial['print_date']
        except Exception:
            formPrintDateInitital = None

        if formPrintDateInitital != formPrintDate:
            self.LIST_FIELDS.append('print date')

        return formPrintDate

    def clean_id_status(self):
        formIDStatus = self.cleaned_data.get('id_status')
        try:
            formIDStatusInitial = self.initial['id_status']
        except Exception:
            formIDStatusInitial = None
        if str(formIDStatusInitial) != str(formIDStatus):
            self.LIST_FIELDS.append('ID status')

        return formIDStatus

    def clean_printer(self):
        formPrinter = self.cleaned_data.get('printer')
        try:
            self.formPrinterInitial = self.initial['printer'].printer
        except Exception:
            try:
                self.formPrinterInitial = self.initial['printer']
            except Exception:
                self.formPrinterInitial = 0

        self.objUsedPrinter = Printers.objects.get(printer_name=formPrinter)

        try:
            objRibbon = RibbonUsageRecord.objects.get(ribbon_number=int(self.instance.ribbon.ribbon_number))
        except Exception:
            objRibbon = None
        if objRibbon is not None:
            if objRibbon.ribbon_status == 'E':
                raise forms.ValidationError(_(
                    'Record cannot be updated. The printer ribbon used by this record is empty.'
                ))

        self.objActiveRibbon = RibbonUsageRecord.objects.filter(
            ribbon_status="A"
        )

        try:
            self.objUsedRibbon = self.objActiveRibbon.get(
                ribbon_printer=formPrinter
            )
        except MultipleObjectsReturned:
            raise forms.ValidationError(_(
                'You have two active ribbons on this printer. ({})'.format(formPrinter)
            ))
        except ObjectDoesNotExist:
            raise forms.ValidationError(_(
                'You have no active ribbon on this printer. ({})'.format(formPrinter)
            ))
        except Exception:
            raise forms.ValidationError(_(
                'Printer error please contact Administrator.'
            ))

        if str(self.formPrinterInitial) != str(formPrinter):
            self.bolPrinterChanged = True
            totalUsedCard = 1 + self.formBadPrint
            self.objUsedRibbon.ribbon_total_printed += totalUsedCard
            self.objUsedPrinter.total_printed += totalUsedCard
            try:
                self.objUsedRibbon.full_clean()
                self.objUsedPrinter.full_clean()
            except Exception:
                raise forms.ValidationError(_('Ribbon or Printer Error.'))
        else:
            if self.bolBadPrintChanged:
                totalCardUsed = int(self.formBadPrintInitial) - int(self.formBadPrint)
                if self.formBadPrint == 0:
                    self.objUsedRibbon.ribbon_total_printed -= int(self.formBadPrintInitial)
                    self.objUsedPrinter.total_printed -= int(self.formBadPrintInitial)
                elif int(self.formBadPrintInitial) > int(self.formBadPrint):
                    self.objUsedRibbon.ribbon_total_printed -= abs(totalCardUsed)
                    self.objUsedPrinter.total_printed -= abs(totalCardUsed)
                else:
                    self.objUsedRibbon.ribbon_total_printed += abs(totalCardUsed)
                    self.objUsedPrinter.total_printed += abs(totalCardUsed)
            try:
                self.objUsedRibbon.full_clean()
                self.objUsedPrinter.full_clean()
            except Exception:
                raise forms.ValidationError(_('Ribbon or Printer Error.'))

        return formPrinter

    # i used a signal pre_delete to do something before deleting
    @receiver(pre_delete, sender=IDPrintRecord)
    def _IDPrintRecord_delete(sender, instance, **kwargs):
        totalCardToReturn = 1 + instance.bad_print
        prevCard = Active_Stocks.objects.get(id=instance.card.id)
        prevRibbonNumber = RibbonUsageRecord.objects.get(ribbon_number=instance.ribbon.ribbon_number)
        prevPrinter = Printers.objects.get(printer_name=instance.printer)
        prevCard.amount += totalCardToReturn
        prevCard.save()
        prevRibbonNumber.ribbon_total_printed -= totalCardToReturn
        prevRibbonNumber.save()
        prevPrinter.total_printed -= totalCardToReturn
        prevPrinter.save()

    def save(self, commit=True):
        instance = super(PrintHistoryForm, self).save(commit=False)
        intFlag = 0
        if instance._state.adding is True:
            self.DICT_MESSAGE['added'] = {}
            intFlag = 1
            instance.ribbon = self.objUsedRibbon
            self.objUsedRibbon.save()
            self.objUsedPrinter.save()
            self.objUsedCard.save()
        else:
            if self.has_changed():
                orig_obj = self._meta.model.objects.get(pk=instance.pk)
                # total the card used
                prevTotalUsedCard = 1 + int(self.formBadPrintInitial)

                if self.bolCardChanged:
                    prevCard = Active_Stocks.objects.get(id=int(self.formCardInitial))
                    prevCard.amount += prevTotalUsedCard
                    prevCard.save()
                    self.objUsedCard.save()
                    self.LIST_FIELDS.append('card type')

                # check if ribbon_number field has changed
                if self.bolPrinterChanged:
                    prevRibbonNumber = RibbonUsageRecord.objects.get(ribbon_number=orig_obj.ribbon.ribbon_number)
                    prevPrinter = Printers.objects.get(printer_name=str(self.formPrinterInitial))
                    prevRibbonNumber.ribbon_total_printed -= prevTotalUsedCard
                    prevPrinter.total_printed -= prevTotalUsedCard
                    prevRibbonNumber.save()
                    prevPrinter.save()
                    instance.ribbon = self.objUsedRibbon
                    self.objUsedRibbon.save()
                    self.objUsedPrinter.save()
                    self.LIST_FIELDS.append('printer')

                if self.bolBadPrintChanged:
                    self.LIST_FIELDS.append('bad print')
                    if not self.bolCardChanged:
                        self.objUsedCard.save()
                    if not self.bolPrinterChanged:
                        instance.ribbon = self.objUsedRibbon
                        self.objUsedRibbon.save()
                        self.objUsedPrinter.save()

                intFlag = 2
                self.DICT_FIELDS['fields'] = self.LIST_FIELDS
                self.DICT_MESSAGE['changed'] = self.DICT_FIELDS

        if commit:
            instance.save()

            if self.request is not None:
                cont_id = ContentType.objects.get_for_model(instance).pk
                if intFlag == 1:
                    act_flag = ADDITION
                else:
                    act_flag = CHANGE

                self.log_actions(
                    cont_id=cont_id,
                    obj_id=smart_text(instance.pk),
                    obj_repr=smart_text(instance),
                    act_flag=act_flag,
                    msg=[self.DICT_MESSAGE],
                )

            self.DICT_MESSAGE.clear()
            self.DICT_FIELDS.clear()
            self.LIST_FIELDS.clear()

        return instance

    def log_actions(self, cont_id, obj_id, obj_repr, act_flag, msg):
        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=cont_id,
            object_id=obj_id,
            object_repr=obj_repr,
            action_flag=act_flag,
            change_message=msg
        )


class SearchForm(forms.Form):
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

    nameSearch = forms.CharField(
        label='Name',
        label_suffix=':',
        required=False,
        max_length=100
    )

    typeSearch = forms.ModelChoiceField(
        label='Card Type',
        label_suffix=':',
        queryset=IDTypes.objects.all(),
        empty_label='All',
        to_field_name='type',
        required=False,
    )

    statusSearch = forms.ChoiceField(
        required=False,
        label='ID Status',
        label_suffix=':',
        choices=(('ALL', 'All'),) + IDPrintRecord.ID_STATUS
    )

    ribbonSearch = forms.IntegerField(
        required=False,
        label='Ribbon No',
        label_suffix='.',
    )

    def clean_dateTo(self):
        dateFrom = self.cleaned_data.get('dateFrom')
        dateTo = self.cleaned_data.get('dateTo')

        if dateFrom > dateTo:
            raise forms.ValidationError(_('Invalid Date.'))

        return dateTo
