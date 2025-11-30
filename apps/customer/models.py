from django.db import models

# Create your models here.


class Customer(models.Model):
    full_name = models.CharField(
        max_length=152, help_text="full name max length=152", blank=True, editable=False
    )
    phone = models.CharField(
        max_length=20, unique=True, help_text="Customer phone number"
    )
    address = models.TextField(blank=True, help_text="Customer address")
    loyalty_points = models.PositiveIntegerField(
        default=0, help_text="Loyalty points earned"
    )
    is_active = models.BooleanField(default=True, help_text="Is the customer active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
