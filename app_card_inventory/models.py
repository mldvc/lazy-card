from django.db import models
from app_overview.models import ID_Card


class ID_Card_Receive_Record(models.Model):
    card = models.ForeignKey(ID_Card, to_field="card_type", on_delete=models.CASCADE)
    rtp_date = models.DateField("RTP Date")
    received_box_amount = models.IntegerField("Box Amount Received")
    received_date = models.DateField("Date Received")
    received_amount = models.IntegerField("Amount Received")

    class Meta:
        verbose_name = "Card Stock Received Record"
        verbose_name_plural = "Card Stock Received Records"
