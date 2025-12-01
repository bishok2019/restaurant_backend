from django.contrib import admin

# Register your models here.
from .models import (
    Employee,
    Kitchen,
    Kitchen_Category,
    Menu,
    MenuItem,
    OrderItem,
    Orders,
)

admin.site.register(
    [
        Employee,
        Kitchen,
        Kitchen_Category,
        Menu,
        MenuItem,
        OrderItem,
        Orders,
    ]
)
