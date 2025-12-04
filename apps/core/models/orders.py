from django.core.validators import MinValueValidator

from base.models import AbstractBaseModel, models


class OrderItem(AbstractBaseModel):
    ITEM_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("served", "Served"),
        ("cancelled", "Cancelled"),
    ]
    DIETARY_CHOICES = [
        ("veg", "Vegetarian"),
        ("non_veg", "Non-Vegetarian"),
        ("vegan", "Vegan"),
        ("gluten_free", "Gluten Free"),
    ]
    SPICE_LEVEL_CHOICES = [
        ("none", "No Spice"),
        ("mild", "Mild"),
        ("medium", "Medium"),
        ("hot", "Hot"),
        ("extra_hot", "Extra Hot"),
    ]
    order = models.ForeignKey(
        "Orders",
        on_delete=models.CASCADE,
        related_name="order_items",  # allows order.order_items.all()
        help_text="The order this item belongs to",
    )
    order_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.PROTECT,
        related_name="order_items",
        help_text="Product being ordered",
    )

    # Quantity & Pricing
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Number of items ordered",
    )

    dietary_type = models.CharField(
        max_length=20,
        choices=DIETARY_CHOICES,
        default="veg",
    )
    spice_level = models.CharField(
        max_length=20,
        choices=SPICE_LEVEL_CHOICES,
        default="none",
    )
    serving_size = models.CharField(
        max_length=100,
        blank=True,
        help_text="Serving size (e.g., '1 plate', '250g')",
    )
    status = models.CharField(
        max_length=20, choices=ITEM_STATUS_CHOICES, default="pending"
    )
    # Timestamps
    prepared_at = models.DateTimeField(
        null=True, blank=True, help_text="When item preparation started"
    )
    ready_at = models.DateTimeField(
        null=True, blank=True, help_text="When item was ready"
    )
    served_at = models.DateTimeField(
        null=True, blank=True, help_text="When item was served"
    )


class Orders(AbstractBaseModel):
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.SET_NULL,
        related_name="orders",
        help_text="Customer who placed the order",
        null=True,
        blank=True,
    )
    order_number = models.CharField(
        max_length=50, unique=True, help_text="Unique order number"
    )
    ORDER_TYPE_CHOICES = [
        ("dine_in", "Dine In"),
        ("takeaway", "Takeaway"),
        ("delivery", "Delivery"),
    ]
    order_type = models.CharField(
        max_length=20, choices=ORDER_TYPE_CHOICES, default="dine_in"
    )

    table_number = models.CharField(
        max_length=20, blank=True, null=True, help_text="Table number (for dine-in)"
    )

    delivery_address = models.TextField(
        blank=True, help_text="Delivery address (for delivery orders)"
    )

    # Status Tracking
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("served", "Served"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    # Payment Information
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("online", "Online"),
        ("wallet", "Digital Wallet"),
    ]
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True
    )

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )

    # Pricing
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Subtotal before tax and discount",
    )
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, help_text="Tax amount"
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, help_text="Discount amount"
    )
    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Delivery charge (if applicable)",
    )

    # Staff Assignment
    served_by = models.ForeignKey(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="served_orders",
        help_text="Staff member who served this order",
    )

    # Timestamps
    confirmed_at = models.DateTimeField(
        null=True, blank=True, help_text="When the order was confirmed"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="When the order was completed"
    )
