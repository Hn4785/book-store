
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    """User model dành cho BookShop."""

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(
        "email address",
        unique=True,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("username"),
                name="accounts_user_username_ci_uniq",
            ),
        ]

    def __str__(self):
        return f"{self.username} ({self.role})"
