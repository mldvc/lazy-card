from django.db import models
from app_overview.models import Active_Stocks
from app_printers.models import Printers
from app_ribbons.models import RibbonUsageRecord
from app_reference.models import IDTypes
from django.core.validators import MinValueValidator


class IDPrintRecord(models.Model):

    ID_STATUS = (
        ('CLA', 'Claimed'),
        ('PRI', 'Printed'),
    )

    id_number = models.CharField("ID No.", max_length=200)
    name = models.CharField("Name", max_length=200)
    id_type = models.ForeignKey(IDTypes)
    bad_print = models.IntegerField("Bad Print")
    print_date = models.DateField("Print Date")
    card = models.ForeignKey(Active_Stocks)
    id_status = models.CharField("ID Status", max_length=3, choices=ID_STATUS, default='CLA')
    printer = models.ForeignKey(Printers, to_field="printer_name")
    ribbon = models.ForeignKey(RibbonUsageRecord, to_field="ribbon_number")

    class Meta:
        verbose_name = "ID Print Record"
        verbose_name_plural = "ID Print Records"
        ordering = ["-id"]
        # permissions = (
        #     ("can_add_all_types", "Add all print types"),
        #     ("can_add_alumni_types", "Add Alumni print types"),
        #     ("can_add_student_types", "Add Student print types"),
        #     ("can_add_employee_types", "Add Employee print types"),
        #     ("can_add_hospital_types", "Add Hospital print types"),
        # )

    def __str__(self):
        return self.name


class CardUsageHistory(models.Model):
    card = models.ForeignKey(Active_Stocks)
    use_date = models.DateField("Use Date")
    amount = models.PositiveIntegerField(
        "Amount",
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "Card Usage Record"
        verbose_name_plural = "Card Usage Reords"

    def __str__(self):
        return self.card.stock_name
