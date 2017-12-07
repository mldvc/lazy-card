from django.db import models
from app_reference.models import Offices


class Printers(models.Model):
    STATUS = (
        ('I', 'Inactive'),
        ('A', 'Active'),
    )

    printer_name = models.CharField(
        "Printer Name",
        max_length=200,
        unique=True
    )
    office = models.ForeignKey(Offices, on_delete=models.CASCADE)
    description = models.TextField("Description")
    status = models.CharField("Status", max_length=1, choices=STATUS)
    total_printed = models.IntegerField("Total Printed")

    class Meta:
        verbose_name = "Printer"
        verbose_name_plural = "Printers"

    def __str__(self):
        return self.printer_name
