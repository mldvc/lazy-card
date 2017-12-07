from django.db import models
from app_overview.models import Printer_Ribbon


class Printer_Ribbon_Receive_Record(models.Model):
    ribbon = models.ForeignKey(Printer_Ribbon, to_field="ribbon_type", on_delete=models.CASCADE)
    rtp_date = models.DateField("RTP Date")
    received_date = models.DateField("Date Received")
    received_amount = models.IntegerField("Amount Received")

    class Meta:
        verbose_name = "Ribbon Stock Received Record"
        verbose_name_plural = "Ribbon Stock Received Records"
