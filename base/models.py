import datetime

import nepali_datetime
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify

from .exceptions import APIError, ModelValidationError


def ad_to_bs_converter(ad_obj):
    date_ad = ad_obj
    year_ad = date_ad.year
    month_ad = date_ad.month
    day_ad = date_ad.day
    date_ad_obj = datetime.date(year_ad, month_ad, day_ad)
    date_bs = nepali_datetime.date.from_datetime_date(date_ad_obj)
    return date_bs


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, hard=False):
        if hard:
            return super().delete()
        return self.update(deleted_at=timezone.now())

    def restore(self):
        return self.update(deleted_at=None)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )

    def hard_delete(self):
        return self.get_queryset().delete(hard=True)


class BranchManager(SoftDeleteManager):
    def get_queryset(self):
        data = super().get_queryset().filter(branch__isnull=False)
        return data


class AbstractSoftDelete(models.Model):
    deleted_at = models.DateTimeField(
        null=True, blank=True, default=None, editable=False
    )
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using, keep_parents)
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class AbstractSlug(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def slug_field(self):
        raise NotImplementedError("Must Implement slug_field")

    __original_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.slug_field

    def save(self, *args, **kwargs):
        if self.slug_field != self.__original_name:
            self.slug = self.unique_slug_generator()
        elif not self.slug:
            self.slug = self.unique_slug_generator()
        super().save(*args, **kwargs)
        self.__original_name = self.slug_field

    def unique_slug_generator(self, new_slug=None):
        """
        This is for a Django project and it assumes your instance
        has a model with a slug field and a title character (char) field.
        """
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(self.slug_field)

        Klass = self.__class__
        qs_exists = Klass.objects.filter(slug=slug).exists()
        if qs_exists:
            new_slug = "{slug}-{id}".format(slug=slug, id=self.pk)
            return self.unique_slug_generator(new_slug=new_slug)
        return slug


class AbstractCreatedByModifiedBy(models.Model):
    """
    An abstract class that provides created_by and modified_by fields.
    """

    created_by = models.IntegerField(default=0, editable=False)
    modified_by = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True


class AbstractCreatedAtModifiedAt(models.Model):
    """
    Abstract class that provides created_at and updated_at fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, editable=False
    )
    created_at_bs = models.CharField(
        max_length=10, blank=True, null=True, editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, editable=False
    )

    class Meta:
        abstract = True


class DeviceApp(models.Model):
    DEVICE_TYPE = (
        ("mobile", "MOBILE"),
        ("pc", "PC"),
        ("tablet", "TABLET"),
        ("other", "OTHER"),
    )
    OS_TYPE = (
        ("windows", "Windows"),
        ("ios", "IOS"),
        ("android", "ANDROID"),
        ("mac", "MAC"),
        ("linux", "LINUX"),
        ("other", "OTHER"),
    )

    device_type = models.CharField(
        max_length=10,
        choices=DEVICE_TYPE,
        default="mobile",
        help_text="Enum field for the device type.",
        editable=False,
    )
    os_type = models.CharField(
        max_length=10,
        choices=OS_TYPE,
        default="other",
        help_text="Enum field for the app type.",
        editable=False,
    )

    class Meta:
        abstract = True


class AbstractBaseModel(
    AbstractCreatedAtModifiedAt,
    AbstractCreatedByModifiedBy,
    AbstractSoftDelete,
    DeviceApp,
):
    """
    Abstract class that provides created_at, modified_at, created_by,
    modified_by and deleted_at fields.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.errors_ = {}
        self.message_ = {}

    def _validate_update_data(self) -> None:
        """
        ### For PATCH/PUT Method
        `validate_update_data` will run if we are performing update operation.\n
        In http language, it's PATCH/PUT method.

        """
        pass

    def _validate_create_data(self) -> None:
        """
        ### For Post Method
        `validate_create_data` will run if we are performing save operation.\n
        In http language, it's POST method.

        """
        pass

    def _validate_required_field(self) -> None:
        """
        ### Will run for both POST/UPDATE method.

        This method will run if the field schema is nullable,
        but still needs restriction to be nullable in db.

        Eg: null=True in model definition,
        but restricted to be nullable from the application.

        More often there might be the case to add field in future
        and we need to add some default or null value.
        We can't stop migrating schemas,
        and can't delete the previous schemas.
        But our application needs to function like this is a required field even
        though its's a new field and nullable allowed.
        """

        pass

    def _validate_unique_together(self):
        """
        This Validation Checks For Any Unique Together validations
        """
        pass

    def _validate_data(self):
        self._validate_required_field()
        self._validate_unique_together()
        if self.pk:
            self._validate_update_data()
        else:
            self._validate_create_data()

    def raise_exception(
        self,
        errors={},
        message={},
        exception_class=None,
    ):
        if errors == {} or message == {}:
            raise ValueError("Please pass message, and errors.")
        if exception_class:
            raise exception_class(errors=errors, message=message)

        raise ModelValidationError(errors=errors, message=message)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        This method will convert ad date to bs date
        """
        if not self.created_at or not self.id:
            self.created_at = timezone.now()
        self.created_at_bs = ad_to_bs_converter(self.created_at)
        self._validate_data()
        super().save(*args, **kwargs)

    @classmethod
    def validate_and_bulk_create(cls, instances, batch_size=None, **kwargs):
        errors = []
        for instance in instances:
            if not instance.id or not instance.created_at_bs:
                if not instance.created_at:
                    instance.created_at = timezone.now()
                instance.created_at_bs = ad_to_bs_converter(instance.created_at)
            try:
                instance.full_clean()
            except ValidationError as e:
                errors.append((instance, e))

        if errors:
            error_messages = {
                str(instance): error.messages for instance, error in errors
            }
            raise ValidationError(f"Validation errors: {error_messages}")

        with transaction.atomic():
            cls.objects.bulk_create(instances, batch_size=batch_size, **kwargs)

        return instances

    class Meta:
        abstract = True
