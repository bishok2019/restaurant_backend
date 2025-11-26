from base.models import AbstractBaseModel, models


class Kitchen_Category(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        blank=True,
        help_text="Description of this kitchen category",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this category currently active?",
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Order in which to display categories",
    )


class Kitchen(AbstractBaseModel):
    kitchen_staff = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        related_name="assigned_kitchen",
        help_text="Employee on this kitchen",
    )
    kitchen_category = models.ForeignKey(
        "Kitchen_Category",
        on_delete=models.PROTECT,
        related_name="kitchen_type",
        help_text="To which kitchen category, this kitchen falls?",
    )
    name = models.CharField(
        max_length=255,
        help_text="Kitchen name/identifier",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Physical location in restaurant (e.g., Ground Floor - Left)",
    )
    max_capacity = models.IntegerField(
        null=True,
        blank=True,
        help_text="Maximum orders this kitchen can handle simultaneously",
    )
