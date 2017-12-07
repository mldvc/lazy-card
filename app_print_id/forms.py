from django import forms
from django.utils.translation import ugettext_lazy as _
from app_id_form.models import ID_Form, FormFields
from django.core.exceptions import ObjectDoesNotExist
from app_reference.models import Departments


class PrintIDForm(forms.ModelForm):
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
            'add_date',
        ]

        labels = {
            'ptn': _('PTN'),
            'ptn_cnum': _('PTN No.'),
            'id_type': _('ID Type'),
            'birth_day': _('DOB'),
            'blood_type': _('BT'),
            'department': _('Dept.'),
            'year_grad': _('Y.Grad'),
            'contact_num': _('Contact#'),
        }

    bolNewPicUpload = False
    bolNewSigUpload = False
    initPicture = None
    initSignature = None
    bolDelPic = False
    bolDelSig = False

    def __init__(self, *args, **kwargs):

        try:
            selected_id = kwargs.pop('selected')
            id_fields = FormFields.objects.exclude(id_type__id=selected_id)
        except KeyError:
            id_fields = None
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

        super(PrintIDForm, self).__init__(*args, **kwargs)
        if id_fields:
            # FOR DEPARTMET FILTERING AND INITIALIZING
            depts = Departments.objects.filter(id_type__id=selected_id)
            self.fields['department'].queryset = depts
            if depts.count() == 1:
                depts = Departments.objects.get(id=depts)
                self.fields['department'].initial = depts.id

            # FILTER FIELDS
            for field in id_fields:
                if str(field.code_name) == 'signature':
                    pass
                elif str(field.code_name) == 'picture':
                    pass
                else:
                    del self.fields["{}".format(field.code_name)]

            # INITAL FOR VALIDITIES IS IN VIEWS.PY

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if self.files.get('picture'):
            picture.name = "pic-{}.jpg".format(self.instance.pk)
            self.bolNewPicUpload = True

        if picture:
            pass
        else:
            self.bolDelPic = True

        try:
            self.initPicture = self.initial['picture']
        except Exception:
            self.initPicture = None

        return picture

    def clean_signature(self):
        signature = self.cleaned_data.get('signature')

        if self.files.get('signature'):
            signature.name = "sig-{}.png".format(self.instance.pk)
            self.bolNewSigUpload = True

        if signature:
            pass
        else:
            self.bolDelSig = True

        try:
            self.initSignature = self.initial['signature']
        except Exception:
            self.initSignature = None

        return signature

    def save(self, commit=True):
        instance = super(PrintIDForm, self).save(commit=False)
        orig_obj = self._meta.model.objects.get(pk=instance.pk)

        if self.bolDelPic:
            orig_obj.picture.delete()

        if self.bolDelSig:
            orig_obj.signature.delete()

        if orig_obj.picture == 'pics/{}'.format(instance.picture):
            if self.bolNewPicUpload:
                orig_obj.picture.delete()

        if orig_obj.signature == 'sigs/{}'.format(instance.signature):
            if self.bolNewSigUpload:
                orig_obj.signature.delete()

        if commit:
            instance.save()
        return instance
