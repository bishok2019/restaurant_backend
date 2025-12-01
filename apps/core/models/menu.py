from base.models import AbstractBaseModel, models
from base.validators.photos import upload_path_user, validate_image


class Menu(AbstractBaseModel):
    """Categories for menu items (e.g., Appetizers, Main Course, Desserts)"""

    name = models.CharField(max_length=255, unique=True, help_text="Category name")
    description = models.TextField(blank=True, help_text="Category description")
    image = models.ImageField(
        upload_to="menu_categories/", null=True, blank=True, help_text="Category image"
    )
    is_active = models.BooleanField(default=True, help_text="Is this category active?")


class MenuItem(AbstractBaseModel):
    """Menu items available in the restaurant"""

    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Product name",
    )
    description = models.TextField(
        help_text="Product description",
    )
    category = models.ForeignKey(
        Menu,
        on_delete=models.PROTECT,
        related_name="product_category",
        help_text="Product category",
    )

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Product price",
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discounted price (if any)",
    )
    photo = models.ImageField(
        upload_to="menu_item/",
        validators=[validate_image],
        blank=True,
        default="default_images/profile.png",
    )

    # Kitchen Assignment
    kitchen = models.ForeignKey(
        "Kitchen",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prepared_from",
        help_text="Which kitchen prepares this Product?",
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Is this Product currently available?",
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Display order within category",
    )
