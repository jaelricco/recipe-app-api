"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):  # Define UserManager based on the BaseUserManager class provided by Django
    """Manager for users."""

    # create_user -> method must be called create_user because its going to be used by different components from Django
    # extrafields -> can provide keyword arguments
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:  # if no email is provided it will raise a ValueError
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # Normalize the email before saving.
        user.set_password(password)
        user.save(using=self._db)  # best practice to save to self._db (in case for multiple databases -> rare tho)

        return user  # return the newly created user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)  # First, create a regular user using the existing create_user method.
        user.is_staff = True  # Grant superuser privileges: this allows bypassing all permission checks.
        user.is_superuser = True  # Grant staff status: this allows access to the Django admin interface. Required to log into the Django admin panel.

        # Save the updated user object to the database.
        # Using `self._db` is best practice for database routing compatibility.
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):  # AbstractBaseUser = Functionality for the auth sytem, PermissionMixin = Functionality for the permissions & fields
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Login with Django Admin

    objects = UserManager()  # Creates instance of our UserManager

    USERNAME_FIELD = 'email'  # Field we wanna use for authentication. Replace the username default field that comes with the default user model
