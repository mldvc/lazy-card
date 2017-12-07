from django.db import models
from app_overview.models import Printer_Ribbon
from app_printers.models import Printers


class RibbonUsageRecord(models.Model):
    STATUS = (
        ('E', 'Empty'),
        ('A', 'Active'),
    )

    ribbon_number = models.IntegerField(
        "Ribbon No.",
        unique=True
    )

    ribbon_type = models.ForeignKey(
        Printer_Ribbon,
        to_field="ribbon_type",
        on_delete=models.CASCADE
    )

    ribbon_printer = models.ForeignKey(
        Printers,
        to_field="printer_name",
        on_delete=models.CASCADE
    )

    ribbon_use_date = models.DateField(
        "Use Date"
    )

    ribbon_status = models.CharField(
        "Status",
        max_length=1,
        choices=STATUS
    )

    ribbon_total_printed = models.IntegerField("Total ID Printed")

    class Meta:
        verbose_name = "Ribbon Usage Record"
        verbose_name_plural = "Ribbon Usage Records"

    def __str__(self):
        return str(self.ribbon_number)
