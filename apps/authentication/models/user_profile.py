from base.models import AbstractBaseModel, models

from .users import CustomUser


class UserProfile(AbstractBaseModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Link to the user this profile belongs to.",
    )
    bio = models.TextField(blank=True, help_text="User biography.")


class OTP(AbstractBaseModel):
    code = models.CharField(
        max_length=50,
        help_text="User code.",
    )
    email = models.EmailField(
        max_length=255,
        help_text="Email address .",
    )
    otp = models.CharField(
        max_length=6,
        help_text="One-time password for verification.",
        unique=True,
    )

    class Meta:
        unique_together = (("email", "code"),)


class ContactUs(AbstractBaseModel):
    name = models.CharField(
        max_length=255,
        help_text="Name of the person contacting us.",
    )
    email = models.EmailField(
        max_length=255,
        help_text="Email address of the person contacting us.",
    )
    subject = models.CharField(
        max_length=255,
        help_text="Subject of the contact message.",
    )

    message = models.TextField(
        help_text="Message from the user.",
    )

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
