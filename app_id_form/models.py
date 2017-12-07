from django.db import models
from app_reference.models import IDTypes, Courses, Strands, Departments, Levels, EmploymentTypes


class ID_Form(models.Model):
    id_type = models.ForeignKey(IDTypes)
    full_name = models.CharField("Name", max_length=200, null=True)
    last_name = models.CharField("Last Name", max_length=100, null=True)
    first_name = models.CharField("First Name", max_length=100, null=True)
    middle_name = models.CharField("Middle Name", max_length=100, null=True)
    blood_type = models.CharField("Blood Type", max_length=10, default='N/A')
    birth_day = models.DateField("Date of Birth")
    contact_num = models.CharField("Contact Number", max_length=100, default='N/A')
    ptn = models.CharField("PTN Incase of Emergency", max_length=100)
    ptn_cnum = models.CharField("PTN Contact Number", max_length=100)
    address = models.CharField("Address", max_length=100)
    level = models.ForeignKey(Levels, null=True)
    strand = models.ForeignKey(Strands, null=True)
    position = models.CharField("Position", max_length=100, null=True)
    emp_type = models.ForeignKey(EmploymentTypes, null=True)
    department = models.ForeignKey(Departments, null=True)
    course = models.ForeignKey(Courses, null=True)
    tin = models.CharField("TIN No.", max_length=200, default='N/A')
    sss = models.CharField("SSS No.", max_length=200, default='N/A')
    id_number = models.CharField("ID No.", max_length=100)
    validity = models.CharField("Validity", max_length=100, null=True)
    picture = models.ImageField("Picture", null=True, blank=True, upload_to='pics')
    signature = models.ImageField("Signature", null=True, blank=True, upload_to='sigs')
    year_grad = models.CharField("Year Graduated", max_length=50, null=True)
    alu_validity = models.CharField("Alumni ID Validity", max_length=100, null=True)
    add_date = models.DateField("Add Date")

    class Meta:
        verbose_name = "ID Forms"
        verbose_name_plural = "ID Forms"

    def __str__(self):
        return self.full_name


class FormFields(models.Model):
    code_name = models.CharField("Code Name", max_length=200)
    name = models.CharField("Name", max_length=200)
    id_type = models.ManyToManyField(IDTypes, blank=True,)

    class Meta:
        verbose_name = "Form Field"
        verbose_name_plural = "Form Fields"

    def __str__(self):
        return self.name
