from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.managers import CustomUserManager
from base.models import AbstractBaseModel, models
from base.validators.photos import upload_path_user, validate_image


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """

    DO NOT raise any model validation error here from the User model.
    That will stop the complete cycle of request and response for
    default panel, & drf panel cycle as we are using CustomErrorMiddleware.
    And will result in an error:
    ```
    The request's session was deleted before the request completed.
    The user may have logged out in a concurrent request, for example.
    ```

    Also, the user may not log in to the admin panel.

    """

    USER_TYPE_CHOICES = (
        ("waiter", "WAITER"),
        ("cleaner", "CLEANER"),
        ("manager", "MANAGER"),
        ("cook", "COOK"),
        ("system", "SYSTEM"),
    )
    GENDER_TYPE = (
        ("male", "MALE"),
        ("female", "FEMALE"),
        ("other", "OTHER"),
    )
    email = models.EmailField(
        max_length=255,
        help_text="Email address. Max Length: 255 characters",
        # unique=True,
        blank=True,
        null=True,
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text="Username must be unique and max_length upto 50 characters",
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="First name can have max_length upto 50 characters, blank=True",
    )
    middle_name = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Middle name can have max_length upto 50 characters, blank=True",
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Last name can have max_length upto 50 characters, blank=True",
    )
    full_name = models.CharField(
        max_length=152, help_text="full name max length=152", blank=True, editable=False
    )
    # designation = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(
        max_length=30,
        choices=GENDER_TYPE,
        default="other",
        help_text="Choices are male, female, and other. Default=male",
    )
    user_type = models.CharField(
        max_length=30,
        choices=USER_TYPE_CHOICES,
        help_text="Choices are school, student, public, system",
    )
    birth_date = models.DateField(
        null=True, blank=True, help_text="Blank=True and null=True"
    )
    # palika = models.ForeignKey(
    #     "location.Palika", on_delete=models.PROTECT, blank=True, null=True
    # )
    palika = models.CharField(
        max_length=100, blank=True, default="", help_text="Municipality name"
    )
    district = models.ForeignKey(
        "location.District", on_delete=models.PROTECT, blank=True, null=True
    )
    ward_no = models.PositiveIntegerField(default=1)
    tole = models.CharField(max_length=100, blank=True, default="")

    mobile_no = models.CharField(
        max_length=15,
        blank=True,
        help_text="Mobile no. should be maximum of 15 characters",
    )
    photo = models.ImageField(
        upload_to=upload_path_user,
        validators=[validate_image],
        blank=True,
        default="default_images/profile.png",
    )

    # --------------- ROLES nad PERMISSIONS
    roles = models.ManyToManyField("authentication.Roles", blank=True)
    permissions = models.ManyToManyField("authentication.CustomPermission", blank=True)
    # ---------------- END ---------------

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"

    # def __str__(self):
    #     return "id {} : {}".format(self.id, self.username)

    @property
    def get_permissions(self):
        return [_.code_name for _ in self.permissions.all()]

    @property
    def get_roles(self):
        return [_.name for _ in self.roles.all()]

    @property
    def get_all_permissions(self):
        return {
            "permissions": self.get_permissions,
            "roles": self.get_roles,
        }

    def tokens(self, request):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_superuser": self.is_superuser,
            "id": self.id,
            **self.get_all_permissions,
        }

    def save(self, *args, **kwargs):
        names = [self.first_name, self.middle_name, self.last_name]
        self.full_name = " ".join(name for name in names if name)
        super().save(*args, **kwargs)
