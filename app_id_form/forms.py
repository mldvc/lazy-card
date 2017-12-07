from django import forms
from .models import ID_Form, FormFields
from app_reference.models import IDTypes, Departments
from datetime import datetime as dt
import datetime
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class FieldsForm(forms.ModelForm):
    class Meta:
        model = FormFields
        fields = ['code_name', 'name', 'id_type']
        widgets = {
            'id_type': forms.CheckboxSelectMultiple,
        }


class SelectTypeForm(forms.Form):
    types = forms.ModelChoiceField(
        label='ID Type',
        label_suffix=':',
        queryset=IDTypes.objects.all(),
        to_field_name='type',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop('request')
        except Exception:
            self.request = None

        super(SelectTypeForm, self).__init__(*args, **kwargs)
        objIDTypes = IDTypes.objects.all()
        if self.request is not None:
            try:
                bolAllIDTypes = self.request.user.userprofile.all_types
            except AttributeError:
                bolAllIDTypes = True

            try:
                officeID = self.request.user.userprofile.printer.office.id
            except AttributeError:
                officeID = None
            print(officeID)
            if bolAllIDTypes is False:
                if officeID is not None:
                    self.fields['types'].queryset = objIDTypes.filter(
                        office__id=officeID
                    )


class IDForm(forms.ModelForm):
    class Meta:
        model = ID_Form

        fields = [
            'id_type',
            'id_number',
            'full_name',
            'last_name',
            'first_name',
            'middle_name',
            'blood_type',
            'birth_day',
            'contact_num',
            'tin',
            'sss',
            'ptn',
            'ptn_cnum',
            'address',
            'department',
            'position',
            'emp_type',
            'course',
            'strand',
            'level',
            'picture',
            'signature',
            'year_grad',
            'validity',
            'alu_validity',
            'add_date'
        ]

        labels = {
            'ptn': _('Person to Notify'),
            'ptn_cnum': _('PTN Contact No.'),
            'id_type': _('ID Type'),
            'emp_type': _('Employment Type'),
        }

    lastName = None
    firstName = None
    middleName = None

    def __init__(self, *args, **kwargs):

        try:
            selected_id = kwargs.pop('selected')
            id_fields = FormFields.objects.exclude(id_type__id=selected_id)
        except KeyError:
            id_fields = None
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

        super(IDForm, self).__init__(*args, **kwargs)
        if id_fields:
            # FOR DEPARTMET FILTERING AND INITIALIZING
            depts = Departments.objects.filter(id_type__id=selected_id)
            self.fields['department'].queryset = depts
            if depts.count() == 1:
                depts = Departments.objects.get(id=depts)
                self.fields['department'].initial = depts.id

            # FILTER FIELDS
            for field in id_fields:
                del self.fields["{}".format(field.code_name)]

            # INITAL FOR VALIDITIES IS IN VIEWS.PY

    def clean_last_name(self):
        self.lastName = self.cleaned_data['last_name']

        return self.lastName.upper()

    def clean_first_name(self):
        self.firstName = self.cleaned_data['first_name']

        return self.firstName.upper()

    def clean_middle_name(self):
        self.middleName = self.cleaned_data['middle_name']

        return self.middleName.upper()

    def clean_full_name(self):
        formName = self.cleaned_data['full_name']

        return formName.upper()

    def clean_blood_type(self):
        bloodType = self.cleaned_data['blood_type']

        return bloodType.upper()

    def clean_ptn(self):
        ptnName = self.cleaned_data['ptn']

        return ptnName.upper()

    def save(self, commit=True):
        instance = super(IDForm, self).save(commit=False)

        if instance._state.adding is True:
            instance.add_date = dt.now()

            # FOR ALUMNI PLUS CARD THAT DOESNT HAVE BIRTH DATE FIELD
            if instance.birth_day is None:
                instance.birth_day = dt.now()

            if instance.full_name is None:
                instance.full_name = '{} {} {}'.format(
                    self.firstName,
                    self.middleName,
                    self.lastName
                )

        else:
            if self.has_changed():
                pass

        if commit:
            instance.save()
        return instance


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

    typeSearch = forms.ModelChoiceField(
        label='ID Type',
        label_suffix=':',
        queryset=IDTypes.objects.all(),
        empty_label='All',
        to_field_name='type',
        required=False,
    )

    nameSearch = forms.CharField(
        label='Name',
        label_suffix=':',
        required=False,
        max_length=100
    )

    def clean_dateTo(self):
        dateFrom = self.cleaned_data.get('dateFrom')
        dateTo = self.cleaned_data.get('dateTo')

        if dateFrom > dateTo:
            raise forms.ValidationError(_('Invalid Date.'))

        return dateTo
