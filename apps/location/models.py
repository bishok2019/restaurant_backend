from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import AbstractBaseModel

from .managers import LocationManager

"""
    Province, District, Location(Palika), Ward
    are set to modesl.PROTECT and AREA is first set to delete in seeder
    because sometimes we need to re-run the location seeder after updating the csv.
    So, to minimize the db conflicts, we have prioritize AREA in first.
    
    The above condition is only applicable while we are on dev environment.
    Once we hit the production, the location seeder should not be re-run.
    
    We need to write the different seeder script to make it
    inline with the production db.

"""


class Province(AbstractBaseModel):
    province_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(_("Name"), max_length=70, unique=True)
    nepali_name = models.CharField(max_length=70, blank=True, default="")
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")


class District(AbstractBaseModel):
    district_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(_("Name"), max_length=50, unique=True)
    nepali_name = models.CharField(max_length=70, blank=True, default="")
    is_active = models.BooleanField(_("Is Active"), default=True)
    province = models.ForeignKey(
        Province, verbose_name=_("Province"), on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")


class Palika(AbstractBaseModel):
    "Also refers as Municipality or VDC"

    location_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(_("Name"), max_length=100)
    nepali_name = models.CharField(max_length=70, blank=True, default="")
    postal_code = models.CharField(
        _("Postal Code"), max_length=10, null=True, blank=True
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        verbose_name=_("District"),
        related_name="locations",
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_deliverable = models.BooleanField(_("Is Deliverable"), default=False)

    objects = LocationManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # self.is_deliverable = self.district.is_active
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        unique_together = ("name", "district")


class Ward(AbstractBaseModel):
    number = models.PositiveSmallIntegerField(_("Number"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    location = models.ForeignKey(
        Palika,
        on_delete=models.PROTECT,
        verbose_name=_("Location"),
        related_name="wards",
    )

    def __str__(self):
        return f"Ward {self.number}"

    class Meta:
        verbose_name = _("Ward")
        verbose_name_plural = _("Wards")
        unique_together = ("number", "location")
