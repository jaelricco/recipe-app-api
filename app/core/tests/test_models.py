"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model  # Helper function -> best practice to use


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'  # 'example.com' is a reserved domain used in documentation and testing.
        password = 'testpass123'  # Define a test password. Since this is for testing, the actual content doesn't matter.
        user = get_user_model().objects.create_user(  # Create a new user using Django's custom user model. 
            email=email,                              # `get_user_model()` returns the currently active User model, which is useful in case you have a custom user model.
            password=password,                        # `objects.create_user()` creates and saves a new user with the given email and password.
        )

        # Check if the email of the created user matches the one we provided.
        # `assertEqual(a, b)` is a test assertion that passes if `a == b`.
        self.assertEqual(user.email, email)

        # Check if the password was correctly set.
        # `check_password(password)` returns True if the given password matches the hashed password stored in the user object.
        # The test will pass if the password check returns True.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        # Define a list of test cases. Each sublist contains:
        # [input_email, expected_normalized_email]
        # Normalization typically means converting the domain part to lowercase.
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],        
        ]

        for email, expected in sample_emails:  # Loop through each email pair in the list.
            user = get_user_model().objects.create_user(email, 'sample123')  # Create a user with the test email and a sample password.

            # Assert that the user's stored email matches the expected normalized version.
            # This ensures that the email normalization logic in the user model works correctly.
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""

        # Create a superuser using the custom user model.
        # This method should automatically set is_superuser=True and is_staff=True.
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        
        # Check if the user has superuser privileges.
        # `is_superuser` is a Boolean field provided by Django’s `PermissionsMixin`.
        # It allows the user to bypass all permission checks.
        self.assertTrue(user.is_superuser)  

        # Check if the user has staff status.
        # `is_staff=True` is required to access the Django admin interface.
        self.assertTrue(user.is_staff)  