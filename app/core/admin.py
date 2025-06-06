"""
Django Admin customization
"""
from django.contrib import admin  # Import Django's admin functionality to customize the admin interface.

# Import the default UserAdmin provided by Django so we can extend and customize it.
# We're renaming it to avoid name conflicts with our custom admin class below.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Import Django's internationalization function to support translated labels in the admin.
# The `_` is the conventional alias used in Django for marking strings for translation.
from django.utils.translation import gettext_lazy as _

from core import models  # Import our custom models from the core app (e.g., custom User model).


class UserAdmin(BaseUserAdmin):  # Define a custom admin class for the User model by extending Django's BaseUserAdmin.
    """Define the admin pages for users."""

    ordering = ['id']  # Set the default ordering of users in the admin list (by ID).

    list_display = ['email', 'name']  # Define which fields to display in the user list page in the admin.

    # Define the layout of fields when viewing/editing a user in the admin.
    # Each tuple defines a section in the form: (Section title, {fields})
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # First section: no title (None), show email and password fields.
        # Permissions section: use a translated title, and include permission-related fields.
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
        (_('Important dates'), {  # Important dates section: show the user's last login.

            'fields': ('last_login',)
        })
    )
    readonly_fields = ['last_login']  # Make the 'last_login' field read-only in the admin interface.
    add_fieldsets = (  # add_fieldsets customizes the layout of the "Add User" form in the Django admin.
        (None, {
            'classes': ('wide',),  # Applies a wider layout style to the form (for better appearance).
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

admin.site.register(models.User, UserAdmin)  # Register the custom User model with the Django admin using the customized UserAdmin class.
