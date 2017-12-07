from django.db import models
from django.core.validators import MinValueValidator
from app_reference.models import Offices
from django.contrib.auth.models import User
from app_printers.models import Printers
from django.db.models.signals import post_save
from django.dispatch import receiver


class ID_Card(models.Model):
    card_type = models.CharField("Card Type", max_length=200, unique=True)
    description = models.TextField("Description")

    amount = models.PositiveIntegerField(
        "Stock Amount",
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "ID Card"
        verbose_name_plural = "ID Cards"

    def __str__(self):
        return self.card_type


class Printer_Ribbon(models.Model):
    ribbon_type = models.CharField("Ribbon Type", max_length=200, unique=True)
    description = models.TextField("Description")

    amount = models.PositiveIntegerField(
        "Stock Amount",
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "Printer Ribbon"
        verbose_name_plural = "Printer Ribbons"

    def __str__(self):
        return self.ribbon_type


class Active_Stocks(models.Model):
    card_type = models.ForeignKey(
        ID_Card, to_field="card_type",
        on_delete=models.CASCADE
    )

    stock_name = models.CharField(
        "Stock Name",
        max_length=200,
        unique=True
    )

    office = models.ForeignKey(Offices, on_delete=models.CASCADE)

    description = models.TextField("Description")

    amount = models.PositiveIntegerField(
        "Stock Amount",
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "Active Stock"
        verbose_name_plural = "Active Stocks"

    def __str__(self):
        return self.stock_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    all_types = models.BooleanField('All ID Types', default=True)
    printer = models.ForeignKey(Printers, null=True, blank=True, on_delete=models.CASCADE)
    active_card = models.ForeignKey(Active_Stocks, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
