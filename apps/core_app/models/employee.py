from base.models import AbstractBaseModel, models


class Employee(AbstractBaseModel):
    user = models.OneToOneField(
        "authentication.CustomUser",
        on_delete=models.CASCADE,
        related_name="employee",
    )
    position = models.CharField(
        max_length=100,
        help_text="Job title/position",
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text="Department (e.g., Kitchen, Service, Management)",
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly salary",
    )
