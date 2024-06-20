"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an emil address.")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Restaurant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField()
    items = models.TextField()

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="votes")
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE,
                            related_name="votes")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "menu")

    def __str__(self):
        return f"{self.employee.email} voted for {self.menu}"
